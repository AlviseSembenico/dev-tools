// Angular
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

// Alert Component
import { AlertModule } from 'ngx-bootstrap/alert';
import { CodeRoutingModule } from './code-routing.module';
import { CodeComponent } from './code.component';

@NgModule({
  imports: [
    CommonModule,
    CodeRoutingModule,
    AlertModule.forRoot(),
  ],
  declarations: [
    CodeComponent
  ]
})
export class CodeModule { }
