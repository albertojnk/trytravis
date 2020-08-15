import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpEventType, HttpRequest, HttpProgressEvent, HttpResponse  } from '@angular/common/http'
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';
import { ProcedureProgress } from './procedure'

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  
  constructor(
    private readonly http: HttpClient
  ) { }

  public uploadFile(form: FormData): Observable<any> {
    return new Observable((success) => {
      const req = new HttpRequest('POST', environment.API_SERVER + '/files', form, {
        reportProgress: true,
      });

      this.http.request(req).subscribe((event: HttpProgressEvent) => {
        if (event.type === HttpEventType.UploadProgress) {
          success.next(event.loaded)
        } else if (event instanceof HttpResponse) {
          success.complete()
        }
      })
    })
  }

  public getCurrentProgress(createdId: string): Observable<ProcedureProgress> {
    return this.http.get<ProcedureProgress>(environment.API_SERVER + '/procedures/' + createdId)
  }
}
