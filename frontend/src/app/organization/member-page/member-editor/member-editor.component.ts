import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MemberService } from '../member.service';
import { MemberDetails } from '../member_details.model';
import { Organization } from '../../organization.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MemberPageComponent } from '../member-page.component';

@Component({
  selector: 'app-member-editor',
  templateUrl: './member-editor.component.html',
  styleUrls: ['./member-editor.component.css']
})
export class MemberEditorComponent implements OnInit {
  public static Route = {
    path: ':slug/members/:id/edit',
    title: 'Member Editor',
    component: MemberEditorComponent
  };

  @Input() organization: Organization | undefined;

  public memberId: any;
  public slug!: string;
  public member: MemberDetails | undefined;
  term: any;
  title = new FormControl('');

  public memberForm = this.formBuilder.group({
    title: this.title
  });

  constructor(
    private memberService: MemberService,
    private route: ActivatedRoute,
    private snackBar: MatSnackBar,
    private permission: PermissionService,
    protected formBuilder: FormBuilder,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.term = params['term'];
    });

    this.slug = this.route.snapshot.params['slug'];
    this.memberId = this.route.snapshot.params['id'];

    if (this.slug && this.memberId) {
      this.fetchMemberById();
    }
  }

  makeAdmin(memberId: any) {
    this.memberService.adminStatus(this.slug!, memberId, this.term).subscribe(
      (data) => {
        this.snackBar.open('Member given Admin Status!', '', {
          duration: 10000
        });

        setTimeout(() => {
          window.location.reload();
        }, 500);
      },
      (error) => {
        console.error('Error making member admin:', error);
        this.snackBar.open('Error making member admin.', '', {
          duration: 10000
        });
      }
    );
  }

  removeAdmin(memberId: any) {
    this.memberService.removeAdmin(this.slug!, memberId, this.term).subscribe(
      (data) => {
        this.snackBar.open('Member removed from Admins', '', {
          duration: 10000
        });

        setTimeout(() => {
          window.location.reload();
        }, 500);
      },
      (error) => {
        console.error('Error removing admin:', error);
        this.snackBar.open('Error removing admin.', '', {
          duration: 10000
        });
      }
    );
  }

  makeLeader(memberId: any) {
    this.memberService.makeLeader(this.slug!, memberId, this.term).subscribe(
      (data) => {
        this.snackBar.open('Member is now a Leader!', '', {
          duration: 10000
        });

        setTimeout(() => {
          window.location.reload();
        }, 500);
      },
      (error) => {
        console.error('Error making member leader:', error);
        this.snackBar.open('Error making member leader.', '', {
          duration: 10000
        });
      }
    );
  }

  removeLeader(memberId: any) {
    this.memberService.removeLeader(this.slug!, memberId, this.term).subscribe(
      (data) => {
        this.snackBar.open('Member is removed from Leaders', '', {
          duration: 10000
        });

        setTimeout(() => {
          window.location.reload();
        }, 500);
      },
      (error) => {
        console.error('Error removing member from Leaders:', error);
        this.snackBar.open('Error removing member from Leaders.', '', {
          duration: 10000
        });
      }
    );
  }

  removeMember(memberId: any) {
    this.memberService.deleteMember(this.slug, memberId, this.term).subscribe(
      (data) => {
        this.snackBar.open('Member removed from organization!', '', {
          duration: 10000
        });

        setTimeout(() => {
          window.location.reload();
        }, 500);
      },
      (error) => {
        console.error('Error removing member:', error);
        this.snackBar.open('Error removing member.', '', {
          duration: 10000
        });
      }
    );
  }

  checkPermissions(): Observable<boolean> {
    return this.permission.check('member.*', `organization/${this.slug}`);
  }

  fetchMemberById(): void {
    this.memberService
      .getMemberById(this.slug, this.term, this.memberId)
      .subscribe({
        next: (data) => {
          this.member = data[0];
        },
        error: (error) => {
          console.error('Error fetching member details:', error);
        }
      });
  }

  onSubmit(): void {
    const updatedMember: MemberDetails = {
      ...(this.member as MemberDetails), // spread the existing member properties into the new object
      ...(this.memberForm.value as Partial<MemberDetails>), // apply form values, potentially overriding properties from this.member
      memberId: this.memberId!
    };
    this.memberService.updateMember(this.slug, updatedMember).subscribe({
      next: (response) => {
        this.member = response; // Update the local member object with the response
        this.onSuccess();
      },
      error: (err) => this.onError(err)
    });
  }

  private onSuccess(): void {
    this.router.navigate(['organizations', this.slug, 'members'], {
      queryParams: { term: this.term }
    });
    this.snackBar.open('Member updated', '', { duration: 2000 });
  }

  onCancel(): void {
    this.router.navigate(['organizations', this.slug, 'members'], {
      queryParams: { term: this.term }
    });
  }

  onError(err: any): void {
    this.snackBar.open('Error! Member not updated', '', {
      duration: 2000
    });
  }
}
