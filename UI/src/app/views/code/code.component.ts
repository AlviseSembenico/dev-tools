import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import ansiStyles from 'ansi-styles';
import * as chalk from 'chalk';
import { NgTerminal } from 'ng-terminal';
import { Observable, Subject } from 'rxjs';
import { CodeService } from './code.service';
import { Snippet } from './interfaces';

@Component({
  selector: 'app-code',
  templateUrl: './code.component.html',
  styleUrls: ['./code.component.scss']
})
export class CodeComponent implements OnInit, AfterViewInit {

  editorOptions = { theme: 'vs-dark', language: 'javascript' };
  snippet: Snippet;
  writeSubject = new Subject<string>();
  editTitle = false;

  @ViewChild('term', { static: true }) terminal: NgTerminal;

  constructor(private codeService: CodeService,
    private router: Router,
    private route: ActivatedRoute) { }

  ngAfterViewInit() {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.codeService.getSnippet(params['id']).subscribe(snippet => {
        this.editorOptions.language = snippet.language.toLowerCase();
        this.snippet = snippet;
      },
        () => this.snippet = {
          name: 'New snippet',
          language: '',
          code: '',
          revision: null
        });
    });
  }

  run() {
    this.codeService.executeSnippet(this.snippet)
      .subscribe(result => {
        this.terminal.underlying.clear();
        if (result.error !== undefined)
          this.writeSubject.next(`${ansiStyles.red.open}${result.error}${ansiStyles.red.close}`);
        this.writeSubject.next(result.res);
      })
  }

  save() {
    if (this.snippet._id)
      this.codeService.saveSnippet(this.snippet).subscribe();
    else {
      this.codeService.createSnippet(this.snippet).subscribe(res => {
        this.snippet._id = res.id;
        // navigate to new snippet with id
        this.router.navigate(['/code', this.snippet._id]);
      });
    }
  }

  saveName() {
    this.editTitle = false;
    this.save();
  }

}
