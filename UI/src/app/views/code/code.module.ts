// Angular
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

// Alert Component
import { AlertModule } from 'ngx-bootstrap/alert';
import { TabsModule } from 'ngx-bootstrap/tabs';
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { CodeRoutingModule } from './code-routing.module';
import { CodeComponent } from './code.component';
import { NgTerminalModule } from 'ng-terminal';
@NgModule({
  imports: [
    CommonModule,
    TabsModule,
    CodeRoutingModule,
    FormsModule,
    NgTerminalModule,
    MonacoEditorModule.forRoot(),
    AlertModule.forRoot(),
  ],
  declarations: [
    CodeComponent
  ]
})
export class CodeModule { }
