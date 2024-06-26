# real-state-ml-pipeline

First run build and up `mysql`, `data-insert` and `model-training` components:

```bash
docker-compose up --build mysql data-insert model-training
```

To insert data into MySQL from a .csv file:

```bash
curl -X POST \
    "http://localhost:8000/properties/from-csv/" \
    -F "file=@data/train.csv"
```

The following return is expected upon execution:

```bash
{
    "message":"16212 properties inserted successfully"
}
```

To run the model training component:

```bash
curl -X GET http://localhost:8001/train
```

The following return is expected:

```bash
{
    "message":"Model trained and saved successfully"
}
```

Now is possible to build and up the `model-inference` component:

```bash
docker-compose up --build model-inference
```

And get model inference:

```bash
curl -X POST \
    "http://localhost:8002/predict" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: 1234567890abcdef1234567890abcdef" \
    -d '{
            "type": "house",
            "sector": "urban",
            "net_usable_area": 120.0,
            "net_area": 150.0,
            "n_rooms": 3,
            "n_bathroom": 2,
            "latitude": 40.7128,
            "longitude": -74.0060
        }'
```

The following return is expected with the price given the input variables:

```bash
{
    "predictions":[10450.683126723623]
}
```



