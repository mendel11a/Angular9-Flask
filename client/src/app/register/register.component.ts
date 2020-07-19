import { Component } from '@angular/core'
import { AuthenticationService, TokenPayload } from '../authentication.service'
import { Router } from '@angular/router'
import { FlashMessagesService } from 'angular2-flash-messages'



@Component({
  templateUrl: './register.component.html'
})
export class RegisterComponent {
  user: TokenPayload = {
    _id: '',
    name: '',
    user_name: '',
    email: '',
    password: ''
  }

  constructor(private auth: AuthenticationService, private router: Router,private flashMessage:FlashMessagesService) {}


  register() {
      // Required Fields
    if(!this.auth.validateRegister(this.user)){
      this.flashMessage.show('Please fill in all fields', {cssClass: 'alert-danger', timeout: 3000})
    }
      // Validate Email
    if(!this.auth.validateEmail(this.user.email)){
      this.flashMessage.show('Please use a valid email', {cssClass: 'alert-danger', timeout: 3000});
    }

    this.auth.register(this.user).subscribe(
      () => {
        this.flashMessage.show('You are now registered and can log in', {cssClass: 'alert-success', timeout: 3000});
        this.router.navigateByUrl('/login');
      },
       err => {
         this.flashMessage.show('Something went wrong', {cssClass: 'alert-danger', timeout: 3000});
        this.router.navigateByUrl('/register');
      })
  }
}