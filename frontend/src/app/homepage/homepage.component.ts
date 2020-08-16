import { Component, OnInit } from '@angular/core';
import { Procedure } from '../procedure'
import { MatTableDataSource } from '@angular/material/table';
import { Angular5Csv } from 'angular5-csv/dist/Angular5-csv';

const URL = "ws://localhost:8000/ws"
const ws = new WebSocket(URL)

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent implements OnInit {
  constructor() {}

  files: File[] = [];
  public isDownloadReady = this.sliceLastXElements(JSON.parse(sessionStorage.getItem('currentData')), 10) !== null ? true : false;
  public progressWidth = 0;
  public dataSource = new MatTableDataSource<Procedure>();;
  public currentData: Procedure[] = this.sliceLastXElements(JSON.parse(sessionStorage.getItem('currentData')), 10);
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
    this.dataSource.data = this.currentData
    // Called whenever there is a message from the server.
    ws.onmessage = (msg) => {
      const response = JSON.parse(msg.data)
      
      this.progressWidth = response.progress
      delete response.progress
      delete response.id
      
      if(this.progressWidth >= 100) {
        this.progressWidth = 0
        this.isDownloadReady = true
      }
      
      this.currentData.push(response)
      sessionStorage.setItem('currentData', JSON.stringify(this.currentData))
      this.populatePreview(this.sliceLastXElements(this.currentData, 10))
    }
    
    // Called if at any point WebSocket API signals some kind of error.
    ws.onerror = (err) => {
      console.log(err)
    }
    
    // Called when connection is closed (for whatever reason).
    ws.onclose = () => {
      console.log('complete') 
    }
  }

  sliceLastXElements(data: Array<any>, x: number): Array<any> {
    if (data == null) {
      return []
    }
    return data.length <= x ? data : data.slice(data.length - x)
  }

  populatePreview(data: Procedure[]) {
    this.dataSource.data = data
  }
  
  onSelect(event) {
      this.files = event.addedFiles;
  }

  refreshTable() {
    this.dataSource.data = this.currentData
  }

  send() {
    const reader = new FileReader();
    new ArrayBuffer(this.files[0].size);
    
    reader.onload = function(e) {
      const rawData = <ArrayBuffer>e.target.result;
      const byteArray = new Uint8Array(rawData);
      ws.send(byteArray.buffer);
    };
    reader.readAsArrayBuffer(this.files[0]);
  }

  download() {
    new Angular5Csv(this.currentData, this.currentData[0].created, { 
      headers: [ ...this.displayedColumns ]
    })

    this.isDownloadReady = false
  }

  onRemove(event) {
      this.files.splice(this.files.indexOf(event), 1);
  }
}
