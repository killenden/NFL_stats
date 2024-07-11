import NFL_stats 
import utils
import NFL_stats.UpdatePlayerDatabase as UpdatePlayerDatabase
import matplotlib.pyplot as plt
import pandas as pd
import os

def export_stats(filename, df):
    if UpdatePlayerDatabase.check_csv_file(filename+'.csv') == False:
        current_dir = os.getcwd()  # Get current working directory
        file_path = os.path.join(current_dir, filename+'.csv')  # Create file path
        os.remove(file_path)


        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, filename)  # Create file path
        df.to_csv(file_path+'.csv', index=False)
    else:
        df = pd.read_csv(filename.endswith('.csv'))

def plots(): 
    rush_df = rush_df[0:10]
    top_ten = rush_df.sort_values('YDS/G', ascending=False)
    plt.bar(top_ten['Player'], top_ten['YDS/G'].astype(float), zorder=2)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Top 10 Rushing Yards Per Game')
    plt.ylabel('Yards Per Game')
    plt.ylim(50, 100)
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/Top_10_Rushing_Yards_Per_Game.png', dpi=450)
    plt.close()

    print(passing_of)
    passing_plays_forty = passing_of.sort_values('40+', ascending=False)
    plt.bar(passing_of.index, passing_of['40+'].astype(float), zorder=2)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Passing Plays of 40+ Yards')
    plt.ylabel('Frequency')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/40yrd_passing_plays.png', dpi=450)
    plt.close()

    passing_plays_twenty = passing_of.sort_values('20+', ascending=False)
    plt.bar(passing_of.index, passing_of['20+'].astype(float), zorder=2)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Passing Plays of 20+ Yards')
    plt.ylabel('Frequency')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/20yrd_passing_plays.png', dpi=450)
    plt.close()

    passing_top_ten = pass_df1.sort_values('YDS/G', ascending=False).head(10)
    plt.bar(passing_top_ten['Player'], passing_top_ten['YDS/G'].astype(float), zorder=2)
    plt.ylim(220, 350)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Top 10 Passing Yards Per Game')
    plt.ylabel('Yards')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/Top_10_Passing_Yards_Per_Game.png', dpi=450)
    plt.close()

    rec_top_ten = rec_df.sort_values('YDS/G', ascending=False).head(10)
    plt.bar(rec_top_ten['Player'], rec_top_ten['YDS/G'].astype(float), zorder=2)
    plt.ylim(50, 100)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Top 10 Recieving Yards Per Game')
    plt.ylabel('Yards')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/Top_10_Recieving_Yards_Per_Game.png', dpi=450)

    team_list = passing_df.index.tolist()
    rushing_df['Team_Name'] = rushing_df.index
    rushing_first_rate = rushing_df['Rush 1st%'].astype(float)
    passing_df['Team_Name'] = passing_df.index
    passing_first_rate = passing_df['1st%'].astype(float)

    first_down_df = pd.merge(rushing_df[['Team_Name', 'Rush 1st%']], passing_df[['Team_Name', '1st%']], on='Team_Name')

    print(first_down_df)

    def get_team_logo(team_abbr):
        current_dir = os.getcwd()
        logo_dir = os.path.join(current_dir,'logos')
        file_path = os.path.join(logo_dir,team_abbr+'.png')
        return file_path

    #Convert columns to float
    first_down_df['Rush 1st%'] = first_down_df['Rush 1st%'].astype('float')
    first_down_df['1st%'] = first_down_df['1st%'].astype('float')

    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(first_down_df['Team_Name']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (first_down_df['Rush 1st%'][i], first_down_df['1st%'][i]), frameon=False)
        ax.add_artist(ab)

    # Set labels and title
    ax.set_xlabel('Rush 1st%')
    ax.set_ylabel('1st%')
    ax.set_title('Scatter Plot of Rush 1st% vs 1st% with Team Logos')

    # Adjust plot limits
    plt.xlim(first_down_df['Rush 1st%'].min() - 1, first_down_df['Rush 1st%'].max() + 1)
    plt.ylim(first_down_df['1st%'].min() - 1, first_down_df['1st%'].max() + 1)
    plt.savefig('logos.png', dpi=450)
    plt.show()
    #plt.close()

if __name__ == '__main__':
    filename = 'stats'

    rush_df, rush_yd_per_gp_df, pass_df, rec_df, rec_rec_per_gp_df, kick_df1, score_df, passing_df, rushing_df, passing_of, rushing_of, output = NFL_stats.NFL_stats()

    export_stats(filename, rush_df)