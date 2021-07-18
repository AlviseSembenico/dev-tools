import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ExecutionResult, Snippet } from './interfaces';

@Injectable({
  providedIn: 'root'
})
export class CodeService {

  constructor(private http: HttpClient) { }

  getSnippet(id: string): Observable<Snippet> {
    return this.http.get<Snippet>(environment.apiUrl + `/snippets/${id}`);
  }

  executeSnippet(snippet: Snippet): Observable<ExecutionResult> {
    return this.http.post<ExecutionResult>(environment.apiUrl + `/snippets/execute`, {
      code: snippet.code,
      language: snippet.language
    });
  }

  saveSnippet(snippet: Snippet): Observable<any> {
    return this.http.put(environment.apiUrl + `/snippets/${snippet._id}`, snippet);
  }

  createSnippet(snippet: Snippet): Observable<any> {
    // Create a new snippet
    return this.http.post(environment.apiUrl + `/snippets`, snippet);
  }

}
