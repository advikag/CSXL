import { Component, Input } from '@angular/core';
import { MemberService } from '../../member-page/member.service';
import { MemberPageComponent } from '../../member-page/member-page.component';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { Profile } from 'src/app/models.module';
import { Organization } from '../../organization.model';
import { Observable } from 'rxjs/internal/Observable';
import { PermissionService } from 'src/app/permission.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrganizationDetailsComponent } from '../../organization-details/organization-details.component';

@Component({
  selector: 'app-member-request-card',
  templateUrl: './member-request-card.component.html',
  styleUrls: ['./member-request-card.component.css']
})
export class MemberRequestCardComponent {
  @Input() memberDetails: any;
  @Input() profile?: Profile;
  @Input() organization?: Organization;

  term: String | undefined;

  slug: string | undefined;
  member: any;
  Array: any;
  constructor(
    private route: ActivatedRoute,
    private memberService: MemberService,
    private permission: PermissionService,
    private snackBar: MatSnackBar,
    private router: Router,
    private organizationService: OrganizationDetailsComponent
  ) {}

  checkPermissions(): Observable<boolean> {
    return this.permission.check('member.*', `organization/${this.slug}`);
  }

  approveMembership(memberId: Number): void {
    this.memberService
      .approveMember(this.organization!.slug, memberId, this.organization!.term)
      .subscribe(
        (data) => {
          this.term = data.term;
          this.snackBar.open('Membership Approved!', '', {
            duration: 10000
          });

          // Set a timeout to refresh the page after the snackbar message is shown
          setTimeout(() => {
            window.location.reload();
          }, 500); //adjust this if you think its too fast
        },
        (error) => {
          console.error('Error approving membership:', error);
          this.snackBar.open('Error approving membership.', '', {
            duration: 10000
          });
        }
      );
  }

  removeMembership(memberId: Number) {
    this.memberService
      .deleteMember(this.organization!.slug, memberId, this.organization!.term)
      .subscribe(
        (data) => {
          this.snackBar.open('Membership Denied!', '', {
            duration: 10000
          });

          setTimeout(() => {
            window.location.reload();
          }, 500);
        },
        (error) => {
          console.error('Error denying membership:', error);
          this.snackBar.open('Error denying membership.', '', {
            duration: 10000
          });
        }
      );
  }

  static Route = {
    path: ':slug/members',
    title: 'Members',
    component: MemberPageComponent
  };
}
