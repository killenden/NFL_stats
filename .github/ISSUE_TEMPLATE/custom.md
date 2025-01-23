---
name: Update Database and Plots
about: This will create a Pull Request that will run the Github Actions to update the database and plots.
title: 'Update Plots and Database'
labels: 'bot'
assignees: ''

---

- type: checkboxes
  attributes:
    label: Update Options
    description: Select the options you want to update.
    options:
      - label: Update Database
        required: false
      - label: Update Plots
        required: false

- type: hidden
  id: update_database
  attributes:
    value: false

- type: hidden
  id: update_plots
  attributes:
    value: false

- type: markdown
  attributes:
    value: |
      This issue will automatically create a pull request with the appropriate title based on the selected options.