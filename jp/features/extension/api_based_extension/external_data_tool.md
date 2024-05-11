# External\_data\_tool

When creating AI applications, developers can use API extensions to incorporate additional data from external tools into prompts as supplementary information for LLMs.

Please read [.](./ "mention") to complete the development and integration of basic API service capabilities.

### Extension Point

`app.external_data_tool.query`: Apply external data tools to query extension points.

This extension point takes the application variable content passed in by the end user and the input content (fixed parameters for conversational applications) as parameters to the API. Developers need to implement the query logic for the corresponding tool and return the query results as a string type.

#### Request Body

```json
{
    "point": "app.external_data_tool.query", 
    "params": {
        "app_id": string,  
        "tool_variable": string,  
        "inputs": {  
            "var_1": "value_1",
            "var_2": "value_2",
            ...
        },
        "query": string | null  
    }
}
```

* Example

```json
{
    "point": "app.external_data_tool.query",
    "params": {
        "app_id": "61248ab4-1125-45be-ae32-0ce91334d021",
        "tool_variable": "weather_retrieve",
        "inputs": {
            "location": "London"
        },
        "query": "How's the weather today?"
    }
}
```

#### API Response

```json
{
    "result": string
}
```

* Example

```json
{
    "result": "City: London\nTemperature: 10°C\nRealFeel®: 8°C\nAir Quality: Poor\nWind Direction: ENE\nWind Speed: 8 km/h\nWind Gusts: 14 km/h\nPrecipitation: Light rain"
}
```

