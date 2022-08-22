# Flood API call data warehousing

<img src="https://media.giphy.com/media/if4XHBAIKurDohCbZF/giphy.gif" width="50px"/>

## Overview

A repository that uses GitHub Actions to schedule the daily request of flood data from the [Environment Agency API](https://www.gov.uk/topic/environmental-management/flooding-coastal-change) and appends to a .csv file. 

## Structure


```
.
├── .github
│   └── api-daily-call.yml
├── data
│   └── flood-data.csv
├── requirements.txt
├── .gitignore
├── get_data.py
├── README.md
└── requirements.txt

```

## Next steps
1. This data will be used in the [flood application](https://github.com/jbuffer/flood-dashboard)
2. The data will be lifted and shifted from a .csv and stored in a postgreSQL database
