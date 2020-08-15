import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomepageComponent } from '../homepage/homepage.component'
import { ProgresspageComponent } from '../progresspage/progresspage.component';

const routes: Routes = [
    {
        path: '',
        component: HomepageComponent,
    },
    {
      path: 'progress',
      component: ProgresspageComponent,
    },
];

@NgModule({
    imports: [
        RouterModule.forRoot(routes)
    ],
    exports: [
        RouterModule
    ],
    declarations: []
})
export class AppRoutingModule { }