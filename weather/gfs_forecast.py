import numpy as np
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
from siphon.catalog import TDSCatalog
import xarray as xr
import metpy
from metpy.units import units
import pandas as pd
from datetime import datetime, timedelta
import requests
from stadium_info import stadium_info_dict

def get_var_safe(ds, varname, time_idx, lat_idx, lon_idx, height_dim=None):
    """
    Safely extract a variable from the GFS dataset with proper error handling.
    
    Parameters:
    - ds: xarray Dataset
    - varname: Name of the variable to extract
    - time_idx, lat_idx, lon_idx: Indices for data extraction
    - height_dim: Optional height dimension name
    
    Returns:
    - Extracted value or None if extraction fails
    """
    try:
        var = ds[varname]
        dims = var.dims

        # Identify time & height dimension names
        time_dim = next((d for d in dims if "time" in d), None)
        height_dim = next((d for d in dims if "height" in d), height_dim)

        # Build isel kwargs
        indexers = {"lat": lat_idx, "lon": lon_idx}
        if time_dim:
            indexers[time_dim] = time_idx
        if height_dim and height_dim in dims:
            indexers[height_dim] = 0  # usually 2m or 10m level

        val = var.isel(**indexers).item()
        return val
    except Exception as e:
        print(f"Missing data for '{varname}': {e}")
        return None


def k_to_f(k):
    """Convert Kelvin to Fahrenheit"""
    return (k - 273.15) * 9 / 5 + 32


def ms_to_mph(ms):
    """Convert meters per second to miles per hour"""
    return ms * 2.23694


def mm_to_inches(mm):
    """Convert millimeters to inches"""
    return mm / 25.4


def fetch_nfl_games():
    """
    Fetch current NFL game schedule from ESPN API.
    
    Returns:
    - List of dictionaries containing game information
    """
    print("Fetching NFL game schedule from ESPN API...")
    
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching NFL data: {e}")
        return []

    game_list = []

    for event in data['events']:
        comp = event['competitions'][0]
        teams = comp['competitors']
        
        home_team = [t['team']['displayName'] for t in teams if t['homeAway'] == 'home'][0]
        away_team = [t['team']['displayName'] for t in teams if t['homeAway'] == 'away'][0]
        
        venue = comp['venue']
        venue_name = venue.get('fullName', 'Unknown Venue')
        location = venue.get('address', {})
        
        city = location.get('city', '')
        state = location.get('state', '')
        country = location.get('country', '')

        kickoff = event['date']

        game_list.append({
            "home_team": home_team,
            "away_team": away_team,
            "venue": venue_name,
            "city": city,
            "state": state,
            "country": country,
            "datetime_utc": kickoff
        })

    print(f"Found {len(game_list)} games")
    return game_list


def get_nfl_weather_forecasts_with_timing(game_list, stadium_info_dict, forecast_hours_ahead=3):
    """
    Get weather forecasts for NFL games using GFS data with detailed timing information
    
    Parameters:
    - game_list: List of games from ESPN API
    - stadium_info_dict: Dictionary with stadium coordinates
    - forecast_hours_ahead: How many hours after kickoff to forecast
    
    Returns:
    - List of dictionaries with game and weather information including GFS timing details
    """
    # Load latest GFS dataset
    print("Loading GFS dataset...")
    tds_gfs = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/Global_0p25deg/latest.html')
    gfs_ds = tds_gfs.datasets[0]
    ds = xr.open_dataset(gfs_ds.access_urls['OPENDAP'])
    ds = ds.metpy.parse_cf()
    
    # Get GFS reference time (model initialization time)
    if 'reftime' in ds.coords:
        gfs_reference_time = pd.to_datetime(ds.reftime.values)
    else:
        # Fallback: estimate from first time step
        gfs_reference_time = pd.to_datetime(ds.time.values[0])
        print("Warning: Could not find reference time, using first forecast time as estimate")
    
    # Ensure reference time is timezone-naive for calculations
    if gfs_reference_time.tz is not None:
        gfs_reference_time = gfs_reference_time.tz_convert('UTC').tz_localize(None)
    
    print(f"GFS Model Run (Reference Time): {gfs_reference_time}")
    print(f"Available forecast hours: 0 to {(pd.to_datetime(ds.time.values[-1]) - gfs_reference_time).total_seconds()/3600:.0f}")
    
    game_forecasts = []
    
    for game in game_list:
        print(f"\nProcessing: {game['away_team']} @ {game['home_team']}")
        
        # Get stadium coordinates
        home_team = game['home_team']
        if home_team not in stadium_info_dict:
            print(f"Stadium info not found for {home_team}")
            continue
            
        stadium = stadium_info_dict[home_team]
        latitude = stadium['latitude']
        longitude = stadium['longitude']
        roof_type = stadium.get('roof_type', 'Open')
        
        # Parse kickoff time
        kickoff_time = pd.to_datetime(game['datetime_utc'])
        forecast_times = [kickoff_time, kickoff_time + pd.Timedelta(hours=forecast_hours_ahead)]
        
        # Find nearest grid indices
        lat_idx = np.abs(ds['lat'].values - latitude).argmin()
        lon_idx = np.abs(ds['lon'].values - longitude).argmin()
        
        # Get forecasts for both times
        forecasts = []
        
        for target_time in forecast_times:
            # Ensure target_time is timezone-naive for consistency
            if target_time.tz is not None:
                target_time = target_time.tz_convert('UTC').tz_localize(None)
            
            # Find closest time index
            time_diffs = np.abs(ds['time'].values - np.datetime64(target_time))
            time_idx = int(np.argmin(time_diffs))
            
            # Get the actual forecast time from the dataset
            actual_forecast_time = pd.to_datetime(ds.time.values[time_idx])
            
            # Ensure forecast time is timezone-naive for calculations
            if actual_forecast_time.tz is not None:
                actual_forecast_time = actual_forecast_time.tz_convert('UTC').tz_localize(None)
            
            # Calculate forecast hour (how many hours ahead of model initialization)
            forecast_hour = (actual_forecast_time - gfs_reference_time).total_seconds() / 3600
            
            # Calculate time difference between requested and actual forecast time
            time_diff_hours = (actual_forecast_time - target_time).total_seconds() / 3600
            
            print(f"  Target: {target_time}")
            print(f"  Actual: {actual_forecast_time} (F{forecast_hour:03.0f}, {time_diff_hours:+.1f}h diff)")
            
            # Extract weather variables
            air_temp = get_var_safe(ds, 'Temperature_height_above_ground', time_idx, lat_idx, lon_idx)
            dew_point = get_var_safe(ds, 'Dewpoint_temperature_height_above_ground', time_idx, lat_idx, lon_idx)
            app_temp = get_var_safe(ds, 'Apparent_temperature_height_above_ground', time_idx, lat_idx, lon_idx)
            u_wind = get_var_safe(ds, 'u-component_of_wind_height_above_ground', time_idx, lat_idx, lon_idx, height_dim='height_above_ground1')
            v_wind = get_var_safe(ds, 'v-component_of_wind_height_above_ground', time_idx, lat_idx, lon_idx, height_dim='height_above_ground1')
            cloud_cover = get_var_safe(ds, 'Total_cloud_cover_entire_atmosphere', time_idx, lat_idx, lon_idx)
            precip = get_var_safe(ds, 'Total_precipitation_surface_Mixed_intervals_Accumulation', time_idx, lat_idx, lon_idx)
            
            # Only process if we have core weather data
            if all(v is not None for v in [air_temp, dew_point, u_wind, v_wind]):
                wind_speed = np.sqrt(u_wind**2 + v_wind**2)
                wind_dir = (270 - np.degrees(np.arctan2(v_wind, u_wind))) % 360
                
                forecast = {
                    "target_time": target_time,
                    "forecast_time": actual_forecast_time,
                    "gfs_reference_time": gfs_reference_time,
                    "forecast_hour": f"F{forecast_hour:03.0f}",
                    "time_diff_hours": round(time_diff_hours, 1),
                    "air_temp_F": round(k_to_f(air_temp), 1),
                    "dew_point_F": round(k_to_f(dew_point), 1),
                    "apparent_temp_F": round(k_to_f(app_temp), 1) if app_temp else None,
                    "wind_speed_mph": round(ms_to_mph(wind_speed), 1),
                    "wind_dir_deg": round(wind_dir, 0),
                    "cloud_cover_pct": round(cloud_cover, 0) if cloud_cover is not None else None,
                    "precip_in": round(mm_to_inches(precip), 2) if precip is not None else 0.0,
                }
                forecasts.append(forecast)
        
        # Create game forecast entry
        if forecasts:
            game_forecast = {
                "game_id": f"{game['away_team']}_at_{game['home_team']}_{kickoff_time.strftime('%Y%m%d')}",
                "away_team": game['away_team'],
                "home_team": game['home_team'],
                "venue": game['venue'],
                "city": game['city'],
                "state": game['state'],
                "kickoff_utc": kickoff_time,
                "kickoff_local": kickoff_time.strftime('%Y-%m-%d %H:%M UTC'),
                "stadium_name": stadium['name'],
                "roof_type": roof_type,
                "latitude": latitude,
                "longitude": longitude,
                "gfs_model_run": gfs_reference_time,
                "kickoff_weather": forecasts[0] if forecasts else None,
                "post_game_weather": forecasts[1] if len(forecasts) > 1 else None
            }
            
            game_forecasts.append(game_forecast)
        else:
            print(f"No weather data available for {home_team}")
    
    return game_forecasts


def assess_weather_impact(weather, roof_type):
    """Assess potential weather impact on the game"""
    impacts = []
    
    # Skip weather impacts for domed/retractable roof stadiums
    if roof_type in ['Closed', 'Retractable']:
        return "Minimal impact (Indoor venue)"
    
    temp = weather['air_temp_F']
    wind = weather['wind_speed_mph']
    precip = weather['precip_in']
    
    # Temperature 
    if temp < 20:
        impacts.append("Extremely cold conditions")
    elif temp < 32:
        impacts.append("Freezing temperatures")
    elif temp > 90:
        impacts.append("Very hot conditions")
    
    # Wind 
    if wind > 20:
        impacts.append("High winds - passing game affected")
    elif wind > 15:
        impacts.append("Moderate winds - kicking affected")
    
    # Precipitation 
    if precip > 0.1:
        impacts.append("Wet field conditions")
    if precip > 0.25:
        impacts.append("Heavy precipitation - significant impact")
    
    return "; ".join(impacts) if impacts else "Favorable conditions"


def display_weather_summary_with_timing(game_forecasts):
    """Display a detailed summary of weather forecasts including GFS timing information"""
    
    if not game_forecasts:
        print("No game forecasts available.")
        return
    
    print(f"\n{'='*90}")
    print(f"NFL WEATHER FORECAST SUMMARY WITH GFS TIMING")
    print(f"{'='*90}")
    
    if game_forecasts:
        gfs_run = game_forecasts[0]['gfs_model_run']
        print(f"GFS Model Run: {gfs_run}")
        print(f"{'='*90}")
    
    for game in game_forecasts:
        print(f"\n{game['away_team']} @ {game['home_team']}")
        print(f"Venue: {game['stadium_name']} ({game['city']}, {game['state']})")
        print(f"Roof Type: {game['roof_type']}")
        print(f"Kickoff: {game['kickoff_local']}")
        
        if game['kickoff_weather']:
            w = game['kickoff_weather']
            print(f"\nKICKOFF WEATHER:")
            print(f"  GFS Forecast: {w['forecast_time']} ({w['forecast_hour']})")
            print(f"  Time Accuracy: {w['time_diff_hours']:+.1f} hours from kickoff")
            print(f"  Temperature: {w['air_temp_F']}°F (Feels like: {w['apparent_temp_F']}°F)")
            print(f"  Wind: {w['wind_speed_mph']} mph from {w['wind_dir_deg']}°")
            print(f"  Cloud Cover: {w['cloud_cover_pct']}%")
            print(f"  Precipitation: {w['precip_in']}\"")
            
            # Weather impact assessment
            impact = assess_weather_impact(w, game['roof_type'])
            if impact:
                print(f"  Impact: {impact}")
        
        if game['post_game_weather']:
            w = game['post_game_weather']
            print(f"\nPOST-GAME WEATHER:")
            print(f"  GFS Forecast: {w['forecast_time']} ({w['forecast_hour']})")
            print(f"  Temperature: {w['air_temp_F']}°F (Feels like: {w['apparent_temp_F']}°F)")
            print(f"  Wind: {w['wind_speed_mph']} mph from {w['wind_dir_deg']}°")
        
        print(f"{'-'*70}")


def create_weather_dataframe_with_timing(game_forecasts):
    """Create a pandas DataFrame with GFS timing information for analysis"""
    rows = []
    
    for game in game_forecasts:
        if game['kickoff_weather']:
            w = game['kickoff_weather']
            row = {
                'game': f"{game['away_team']} @ {game['home_team']}",
                'venue': game['stadium_name'],
                'city': game['city'],
                'state': game['state'],
                'roof_type': game['roof_type'],
                'kickoff_utc': game['kickoff_utc'],
                'gfs_model_run': game['gfs_model_run'],
                'forecast_hour': w['forecast_hour'],
                'time_accuracy_hrs': w['time_diff_hours'],
                'temp_f': w['air_temp_F'],
                'feels_like_f': w['apparent_temp_F'],
                'wind_mph': w['wind_speed_mph'],
                'wind_dir': w['wind_dir_deg'],
                'cloud_cover_pct': w['cloud_cover_pct'],
                'precip_in': w['precip_in'],
                'weather_impact': assess_weather_impact(w, game['roof_type'])
            }
            rows.append(row)
    
    return pd.DataFrame(rows)


def save_results_to_csv(weather_df, filename=None):
    """Save weather forecast results to CSV file"""
    import os
    forecasts_dir = os.path.join(os.path.dirname(__file__), 'gfs_forecasts')
    os.makedirs(forecasts_dir, exist_ok=True)
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"{timestamp}_nfl_forecast.csv"
    # Ensure the file is saved in the forecasts directory
    full_path = os.path.join(forecasts_dir, filename)
    weather_df.to_csv(full_path, index=False)
    print(f"Results saved to: {full_path}")
    return full_path


def main():
    """Main execution function"""
    print("NFL Weather Forecast Script")
    print("=" * 50)
    
    try:
        game_list = fetch_nfl_games()
        if not game_list:
            print("No games found. Exiting.")
            return
        
        print("\nGetting weather forecasts with detailed GFS timing information...")
        nfl_weather_with_timing = get_nfl_weather_forecasts_with_timing(
            game_list, 
            stadium_info_dict, 
            forecast_hours_ahead=3
        )
        
        if not nfl_weather_with_timing:
            print("No weather forecasts could be generated. Exiting.")
            return
        
        display_weather_summary_with_timing(nfl_weather_with_timing)
        weather_timing_df = create_weather_dataframe_with_timing(nfl_weather_with_timing)
        
        print(f"\nEnhanced DataFrame with {len(weather_timing_df)} games:")
        print(weather_timing_df[['game', 'gfs_model_run', 'forecast_hour', 'time_accuracy_hrs', 'temp_f', 'wind_mph']].head())
        
        csv_filename = save_results_to_csv(weather_timing_df)
        
        print(f"\nSUMMARY STATISTICS:")
        print(f"Average temperature: {weather_timing_df['temp_f'].mean():.1f}°F")
        print(f"Average wind speed: {weather_timing_df['wind_mph'].mean():.1f} mph")
        print(f"Games with precipitation: {(weather_timing_df['precip_in'] > 0.1).sum()}")
        print(f"Indoor venues: {(weather_timing_df['roof_type'].isin(['Closed', 'Retractable'])).sum()}")
        
        return weather_timing_df
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        raise


if __name__ == "__main__":
    print("=" * 50)
    print("Starting NFL Weather Forecast Script...")
    print("=" * 50)
    weather_df = main()
    print("=" * 50)
    print("NFL Weather Forecast Script completed.")
    print("=" * 50)
