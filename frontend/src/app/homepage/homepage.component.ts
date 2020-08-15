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
  constructor(
    private apiService: ApiService
    ) {}
  files: File[] = [];
  formData = new FormData();
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
    'passiva',
    'e_ativa',
    'e_passiva',
    'created',
  ];

  ngOnInit(): void {
    this.refreshTable()
    
    // Called whenever there is a message from the server.
    ws.onmessage = (msg) => {
      this.currentData.push(JSON.parse(msg.data))
      this.refreshTable()
      console.log(this.dataSource.data);
    }
    
    ws.onerror = (err) => {
      console.log(err) // Called if at any point WebSocket API signals some kind of error.
    }
    
    ws.onclose = () => console.log('complete') // Called when connection is closed (for whatever reason).
  }


  onSelect(event) {
      this.files = event.addedFiles;
  }

  refreshTable() {
    this.dataSource.data = this.currentData
  }

  send() {
    // this.formData.append("file", this.files[0]);
    this.showProgressBar = true;
    
    const reader = new FileReader();
    const rawData = new ArrayBuffer(this.files[0].size);
    
    reader.onload = function(e) {
      const rawData = <ArrayBuffer>e.target.result;
      const byteArray = new Uint8Array(rawData);
      console.log(byteArray.buffer);
      
      ws.send(byteArray.buffer);
    };
    reader.readAsArrayBuffer(this.files[0]);
    
  }

  onRemove(event) {
      console.log(event);
      this.files.splice(this.files.indexOf(event), 1);
  }
}
