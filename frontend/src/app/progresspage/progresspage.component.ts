import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service'
import { Procedure } from '../procedure'
import { MatTableDataSource } from '@angular/material/table';
import { Angular5Csv } from 'angular5-csv/dist/Angular5-csv';

@Component({
  selector: 'app-progresspage',
  templateUrl: './progresspage.component.html',
  styleUrls: ['./progresspage.component.scss']
})
export class ProgresspageComponent implements OnInit {

  constructor(
    private apiService: ApiService,
  ) { }

  csv: string[] = [];
  public isDownloadReady = JSON.parse(sessionStorage.getItem('progressData')) !== null ? true : false;
  public progressWidth = 0;
  public createdId = '';
  public showTable = JSON.parse(sessionStorage.getItem('progressData')) !== null ? true : false;
  public progressData: Procedure[] = JSON.parse(sessionStorage.getItem('progressData'));
  public dataSource = new MatTableDataSource<Procedure>();;
  public displayedColumns: string[] = [
    'created',
    'consultado',
    'extraido',
    'comarca',
    'o_julgador',
    'procedimento',
    'ativa',
    'e_ativa',
    'passiva',
    'e_passiva',
  ];

  ngOnInit(): void {
    this.dataSource.data = this.progressData
  }

  async send() {
    const res = await this.apiService.getCurrentProgress(this.createdId).toPromise()
    for (let i = 0; i < res.procedures.length; i++) {
      delete res.procedures[i].id
    }
    this.dataSource.data = res.procedures
    sessionStorage.setItem('progressData', JSON.stringify(res.procedures))

    this.showTable = true
    this.isDownloadReady = true
  }

  download() {
    const csv = new Angular5Csv(this.dataSource.data, this.dataSource.data[0].created, { 
      headers: [ ...this.displayedColumns ]
    })

    this.isDownloadReady = false
  }

  clear() {
    sessionStorage.removeItem('progressData')
    this.dataSource.data = []
    this.progressData = []
    this.showTable = false
    this.isDownloadReady = false
  }
}
