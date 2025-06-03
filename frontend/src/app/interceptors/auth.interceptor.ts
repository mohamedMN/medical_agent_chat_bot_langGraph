import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const currentUser = this.authService.currentUser$.value;

    if (currentUser?.accessToken) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${currentUser.accessToken}`
        }
      });
    }

    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401 && currentUser?.refreshToken) {
          return this.authService.refreshToken().pipe(
            switchMap(() => {
              const updatedUser = this.authService.currentUser$.value;
              request = request.clone({
                setHeaders: {
                  Authorization: `Bearer ${updatedUser?.accessToken}`
                }
              });
              return next.handle(request);
            })
          );
        }
        return throwError(() => error);
      })
    );
  }
}