import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service'
import { Procedure } from '../procedure'
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-progresspage',
  templateUrl: './progresspage.component.html',
  styleUrls: ['./progresspage.component.scss']
})
export class ProgresspageComponent implements OnInit {

  constructor(
    private apiService: ApiService,
  ) { }

  public progressWidth = 0;
  public createdId = '';
  public showTable = false;
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
    console.log(20200815182214);
  }

  async send() {
    const res = await this.apiService.getCurrentProgress(this.createdId).toPromise()
    this.dataSource.data = res.procedures
    this.showTable = true
  }
}
