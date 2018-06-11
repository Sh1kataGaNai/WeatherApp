import { Component } from '@angular/core';
import {ForecastService} from "./forecast.service";
import { interval } from 'rxjs/observable/interval';
import { takeWhile, tap } from 'rxjs/operators';
import { IntervalObservable} from "rxjs/observable/IntervalObservable";


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [ForecastService]
})
export class AppComponent {
  constructor(private forecastService: ForecastService) {}
  show_city_component = false
  data = {}
  city_input  = ''
  country_code_input = ''
  date_forecast_input = ''
  isFinished = false
  current = 0;
  interval_polling;

  getForecast(){
    this.forecastService.getData(this.country_code_input, this.city_input, this.date_forecast_input)
      .subscribe(forecast=>{
        console.log(forecast)
        if((forecast as any).db_exists_forecast == true && (forecast as any).db_exists_city == true) {

          this.data = forecast
          this.show_city_component = true

        }
        else{
          if(forecast.hasOwnProperty('task_track_id') && (forecast as any).message == 'Success'){

            this.isFinished = false;
            console.log('Start tracking task with id ' + (forecast as any).task_track_id)

            this.interval_polling = setInterval(() =>{
              this.current += 1
              console.log('Current time of interval polling task: ' + this.current)
              let task_track_id = (forecast as any).task_track_id
              this.forecastService.getTaskStatus(task_track_id).subscribe(resp =>{
                if ((resp as any).task_status == 'SUCCESS'){
                  if((resp as any).task_result.hasOwnProperty('city')) {
                    this.isFinished = true
                    this.current = 0
                    this.data = (resp as any).task_result
                    this.show_city_component = true
                    console.log('Task success')
                    clearInterval(this.interval_polling)
                  }
                  else{
                    let message = (resp as any).task_result
                    console.log(message)
                    alert(message)
                    this.isFinished = true;
                    this.current = 0;
                    clearInterval(this.interval_polling)
                  }
                }
                else if ((resp as any).task_status == 'RETRY'){
                  let message = 'Something went wrong, retrying...'
                  console.log(message)
                  alert(message)
                }
                else if ((resp as any).task_status == 'FAILED'){
                  let message = 'Task has been failed, try later or contact site admin.'
                  console.log(message)
                  alert(message)
                  this.isFinished = true;
                  this.current = 0;
                  clearInterval(this.interval_polling)
                }
              })
            }, 500)

          }
        }
      },
        error2 => {
        if(error2.error.hasOwnProperty('required_date_search')){
          let message = (error2.error as any).required_date_search[0]
            console.log(message)
            alert(message)
        }
        else if (error2.error.hasOwnProperty('iso_country_code')){
          let message = 'country_code: ' + (error2.error as any).iso_country_code[0]
          console.log(message)
          alert(message)
        }
        else{
          console.log(error2.error)
          alert('Unknown error')
        }

      }
      )
  }

}
