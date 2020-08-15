import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpEventType, HttpRequest, HttpProgressEvent, HttpResponse  } from '@angular/common/http'
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  
  constructor(
    private readonly http: HttpClient
  ) { }

  public putData(form: FormData, fileSize: number): Observable<any> {
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
}
