import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs/Observable";

@Injectable()
export class ForecastService {

  constructor(private HttpClient: HttpClient) { }
  raw_data = {}

  public getData(country_code: string, city: string, forecast_date: string)  {
    return this.HttpClient.get('http://127.0.0.1:8000/weather_forecast' +
      '/'+ country_code + '/' + city + '/' + forecast_date)

  }
  public getTaskStatus(task_id: string){
    return this.HttpClient.get('http://127.0.0.1:8000/task_status/' + task_id)
  }




}
