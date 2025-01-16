---
name: Custom issue template
about: Describe this issue template's purpose here.
title: ''
labels: ''
assignees: ''

---

- type: dropdown
  attributes:
    label: Update Information
    description: Do you want to update the database and plots?
    multiple: false
    options:
      - Yes (Default)
      - No
    default: 0
  validations:
    required: true
