import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService } from '../api.service';
import { Procedure } from '../procedure'
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent implements OnInit {
  constructor(
    private apiService: ApiService
    ) {}
    
  files: File[] = [];
  formData = new FormData();
  public showProgressBar = false;
  public progressWidth = 0;
  public dataSource = new MatTableDataSource<Procedure>();;
  public displayedColumns: string[] = [
    'consultado',
    'extraido',
    'comarca',
    'o_julgador',
    'procedimento',
    'ativa',
    'passiva',
    'e_ativa',
    'e_passiva',
    'created',
  ];

  ngOnInit(): void {
    this.refreshTable()
    console.log(this.dataSource.data);
  }


  onSelect(event) {
      this.files = event.addedFiles;
  }

  refreshTable() {
    this.dataSource.data = [
      { 
        consultado: '1',
        extraido: '2',
        comarca: '3',
        o_julgador: '4',
        procedimento: '5',
        ativa: '6',
        passiva: '7',
        e_ativa: '8',
        e_passiva: '9',
        created: '10'
      }
    ];
  }

  send() {
    // this.formData.append("file", this.files[0]);
    // this.showProgressBar = true;

    // this.apiService.uploadFile(this.formData).subscribe(progress => {
    //   this.progressWidth = Math.round(progress / this.files[0].size * 100);
    // }).add(() => {
    //   this.showProgressBar = false;
    //   this.progressWidth = 0;
    // })
  }

  onRemove(event) {
      console.log(event);
      this.files.splice(this.files.indexOf(event), 1);
  }
}
