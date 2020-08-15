import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService } from '../api.service';
import { Procedure } from '../procedure'
import { MatTableDataSource } from '@angular/material/table';


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
  public showProgressBar = false;
  public progressWidth = 0;
  public dataSource = new MatTableDataSource<Procedure>();;
  public currentData: Procedure[] = [];
  public displayedColumns: string[] = [
    'consultado',
    'extraido',
    'comarca',
    'o_julgador',
    'procedimento',
    'ativa',
    'e_ativa',
    'passiva',
    'e_passiva',
    'created',
  ];

  ngOnInit(): void {
    // Called whenever there is a message from the server.
    ws.onmessage = (msg) => {
      if(this.currentData.length === 10) {
        this.currentData = this.currentData.slice(1)
      }
      const response = JSON.parse(msg.data)
      
      this.progressWidth = response.progress
      delete response.progress

      if(this.progressWidth >= 100) {
        this.resetPrograssBar()
      }

      this.currentData.push(response)
      this.populatePreview(this.currentData)
    }
    
    // Called if at any point WebSocket API signals some kind of error.
    ws.onerror = (err) => {
      console.log(err)
    }
    
    // Called when connection is closed (for whatever reason).
    ws.onclose = () => {
      this.showProgressBar = false
      console.log('complete') 
    }
  }

  populatePreview(data: Procedure[]) {
    this.dataSource.data = data
  }
  
  onSelect(event) {
      this.files = event.addedFiles;
  }

  send() {
    this.showProgressBar = true;
    
    const reader = new FileReader();
    new ArrayBuffer(this.files[0].size);
    
    reader.onload = function(e) {
      const rawData = <ArrayBuffer>e.target.result;
      const byteArray = new Uint8Array(rawData);
      ws.send(byteArray.buffer);
    };
    reader.readAsArrayBuffer(this.files[0]);
  }

  onRemove(event) {
      this.files.splice(this.files.indexOf(event), 1);
  }

  resetPrograssBar() {
    this.showProgressBar = false
    this.progressWidth = 0
  }
}
