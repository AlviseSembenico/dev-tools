import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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

  @ViewChild('term', { static: true }) terminal: NgTerminal;

  constructor(private codeService: CodeService,
    private route: ActivatedRoute) { }

  ngAfterViewInit() {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.codeService.getSnippet(params['id']).subscribe(snippet =>
        this.snippet = snippet);
    });
  }

  run() {
    this.codeService.executeSnippet(this.snippet)
      .subscribe(result => {
        this.terminal.underlying.clear();
        if (result.error !== undefined)
          this.writeSubject.next(`${ansiStyles.red.open}chalk.red(result.error)${ansiStyles.red.close}`);
        this.writeSubject.next(result.res);
      })
  }

}
