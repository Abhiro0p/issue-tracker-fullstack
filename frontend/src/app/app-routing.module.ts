import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { IssueListComponent } from './components/issue-list/issue-list.component';

const routes: Routes = [
  { path: '', component: IssueListComponent },
  { path: 'issues', component: IssueListComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }