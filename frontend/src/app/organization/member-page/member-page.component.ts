// member-page.component.ts
import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MemberService } from './member.service';
import { Profile } from 'src/app/models.module';
import { Observable, of } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PermissionService } from 'src/app/permission.service';
import { Organization } from '../organization.model';
import { MemberDetails } from './member_details.model';

@Component({
  selector: 'app-member-page',
  templateUrl: './member-page.component.html',
  styleUrls: ['./member-page.component.css']
})
export class MemberPageComponent implements OnInit {
  organization: Organization | undefined;
  slug!: string;
  memberDetails: MemberDetails[] | undefined;
  leaderDetails: any[] = [];
  member: any;
  Array: any;
  selectedMemberId!: number;
  term: any;
  allMembers: any[] = []; 
  admin_status!: boolean;
  menu: any;

  constructor(
    private route: ActivatedRoute,
    private memberService: MemberService,
    private snackBar: MatSnackBar,
    private permission: PermissionService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      // gets the term from the query parameters
      this.term = params['term'];
    });

    this.route.paramMap.subscribe((params) => {
      this.slug = params.get('slug')!;
      if (this.slug) {
        this.fetchMemberDetails();
        this.fetchLeaderDetails();
      }
    });
  }

  fetchMemberDetails(): void {
    // displays members of an organization
    this.memberService.getApprovedMembers(this.slug!, this.term).subscribe({
      next: (data) => {
        this.memberDetails = data;
      },
      error: (error) => {
        console.error('Error fetching member details:', error);
      }
    });
  }

  fetchLeaderDetails(): void {
    // displays leaders of an organization
    this.memberService.getLeaders(this.slug!, this.term).subscribe({
      next: (data) => {
        this.leaderDetails = data;
      },
      error: (error) => {
        console.error('Error fetching leader details:', error);
      }
    });
  }

  makeAdmin(memberId: Number) {
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

  removeAdmin(memberId: Number) {
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

  static Route = {
    path: ':slug/members',
    title: 'Members',
    component: MemberPageComponent
  };

  checkPermissions(): Observable<boolean> {
    return this.permission.check('member.*', `organization/${this.slug}`);
  }
}
