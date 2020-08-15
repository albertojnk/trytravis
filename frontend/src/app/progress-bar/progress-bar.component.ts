import { Component, Input, OnChanges } from '@angular/core';

@Component({
  selector: 'app-progress-bar',
  templateUrl: './progress-bar.component.html',
  styleUrls: ['./progress-bar.component.scss']
})
export class ProgressBarComponent implements OnChanges {

  @Input() progressWidth: number;

  public showProgressBar = false;

  constructor() { }

  ngOnChanges(): void {
    if (this.progressWidth > 0) {
      this.showProgressBar = true
    }
    if(this.progressWidth >= 100 || this.progressWidth === 0) {
      this.showProgressBar = false
      this.progressWidth = 0
    }
  }
  
}
