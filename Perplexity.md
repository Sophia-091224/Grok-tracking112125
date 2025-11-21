Here is a summarized table of key visualization graphics components for food product traceability (using eggs as an example), followed by three mock datasets in JSON format for those components.

| Visualization Component       | Description                                                      | Example Fields                              |
|-------------------------------|------------------------------------------------------------------|---------------------------------------------|
| Source Provider               | Information about the egg farm or production site                | Provider name, farm ID, location             |
| Distributor                  | Details of entity distributing the eggs                          | Distributor name, ID, location               |
| Production Date              | Date when eggs were laid or collected                             | Production date (YYYY-MM-DD)                  |
| Distribution Date            | Date eggs were shipped or distributed                             | Distribution date (YYYY-MM-DD)                |
| Batch Number                 | Unique identifier for a specific batch of eggs                   | Batch number or code                          |
| Certification/Quality Status | Organic certification, safety status, or quality control notes  | Certification type, inspection dates         |
| Transaction Records          | History of transfers along the supply chain                      | From, To, Date, Quantity                      |

***

### Mock Datasets (JSON)

```json
[
  {
    "batchNumber": "BATCH12345",
    "sourceProvider": {
      "name": "Green Farm Co.",
      "farmID": "GF001",
      "location": "Iowa, USA"
    },
    "distributor": {
      "name": "Fresh Eggs Logistics",
      "distributorID": "DEL100",
      "location": "Chicago, USA"
    },
    "productionDate": "2025-11-10",
    "distributionDate": "2025-11-15",
    "certification": {
      "type": "Organic",
      "inspectionDate": "2025-11-05"
    },
    "transactionHistory": [
      {"from": "Green Farm Co.", "to": "Fresh Eggs Logistics", "date": "2025-11-15", "quantity": 5000}
    ]
  },
  {
    "batchNumber": "BATCH67890",
    "sourceProvider": {
      "name": "Sunny Side Farms",
      "farmID": "SSF002",
      "location": "Nebraska, USA"
    },
    "distributor": {
      "name": "Egg Distributors Inc.",
      "distributorID": "EDI200",
      "location": "Denver, USA"
    },
    "productionDate": "2025-11-12",
    "distributionDate": "2025-11-18",
    "certification": {
      "type": "Free-range",
      "inspectionDate": "2025-11-10"
    },
    "transactionHistory": [
      {"from": "Sunny Side Farms", "to": "Egg Distributors Inc.", "date": "2025-11-18", "quantity": 8000}
    ]
  },
  {
    "batchNumber": "BATCH54321",
    "sourceProvider": {
      "name": "Happy Hen Organic",
      "farmID": "HHO003",
      "location": "Vermont, USA"
    },
    "distributor": {
      "name": "North East Egg Co.",
      "distributorID": "NEEC300",
      "location": "Boston, USA"
    },
    "productionDate": "2025-11-08",
    "distributionDate": "2025-11-14",
    "certification": {
      "type": "Organic",
      "inspectionDate": "2025-11-07"
    },
    "transactionHistory": [
      {"from": "Happy Hen Organic", "to": "North East Egg Co.", "date": "2025-11-14", "quantity": 6000}
    ]
  }
]
```

This table and datasets provide a structured way to visualize key traceability points for egg products, suitable for creating graphics such as supply chain flowcharts, batch tracking timelines, or certification status dashboards.[1][5][7]

[1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11166310/)
[2](https://www.itu.int/en/ITU-D/Regional-Presence/Europe/Documents/Publications/2023/ITU-FAO_StocktakingReport_DigitalExcellenceinAgriculture_EuropeandCentralAsia_CallforGoodPractices_05July.pdf)
[3](https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2024.1389945/full)
[4](https://www.kaggle.com/code/prateekiet/text-analysis)
[5](https://wiki.openfoodfacts.org/Food_Traceability_Codes/Eggs)
[6](https://huggingface.co/spaces/allenai/WildBench/commit/65936793fc2fd565a03278d6cff57612396adae2.diff?file=WildBench-main%2Feval_results%2Fv2.0625%2Fscore.v2%2Feval%3Dgpt-4o-2024-05-13%2FNous-Hermes-2-Mixtral-8x7B-DPO.json)
[7](https://www.wearenewcode.com/industries/food-and-beverage/egg-coding-and-marking-systems)
[8](https://pure.qub.ac.uk/files/529406237/Yunhe_Thesis_After_viva_Final_submittion_V3.pdf)
[9](https://www.sciencedirect.com/science/article/pii/S0924224425002900)
[10](https://publications.rwth-aachen.de/record/464316/files/464316.pdf)
