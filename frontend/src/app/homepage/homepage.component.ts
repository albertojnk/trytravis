import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ApiService } from '../api.service'

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent implements OnInit {
  constructor(
    private http: HttpClient,
    private apiService: ApiService
    ) {}

  public showProgressBar = false;
  public progressWidth = 0;

  ngOnInit(): void {}

  files: File[] = [];
  formData = new FormData();

  onSelect(event) {
      this.files = event.addedFiles;
  }

  send() {
    console.log(this.files);
    this.formData.append("myFile", this.files[0]);
    this.showProgressBar = true;

    this.apiService.putData(this.formData, this.files[0].size).subscribe(progress => {
      this.progressWidth = Math.round(progress / this.files[0].size * 100);
      console.log(this.progressWidth);
    }).add(() => {
      this.showProgressBar = false;
      this.progressWidth = 0;
    })
    
  }

  onRemove(event) {
      console.log(event);
      this.files.splice(this.files.indexOf(event), 1);
  }
}
