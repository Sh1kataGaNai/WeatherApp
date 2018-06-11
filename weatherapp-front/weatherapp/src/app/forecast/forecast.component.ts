import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-forecast',
  templateUrl: './forecast.component.html',
  styleUrls: ['./forecast.component.scss']
})
export class ForecastComponent implements OnInit {

  @Input() forecast;
  weather_icon = ''
  constructor() { }

  ngOnInit() {
    this.weather_icon = 'http://openweathermap.org/img/w/' + this.forecast.weather_icon + '.png';
  }

}
