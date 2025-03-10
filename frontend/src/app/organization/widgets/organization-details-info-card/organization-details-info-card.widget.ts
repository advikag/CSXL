/**
 * The Organization Details Info Card widget abstracts the implementation of each
 * individual organization detail card from the whole organization detail page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';
import { map } from 'rxjs/operators';
import { Organization } from '../../organization.model';
import { Profile } from 'src/app/profile/profile.service';
import { PermissionService } from 'src/app/permission.service';
import { Observable } from 'rxjs';
import { MemberService } from '../../member-page/member.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'organization-details-info-card',
  templateUrl: './organization-details-info-card.widget.html',
  styleUrls: ['./organization-details-info-card.widget.css']
})
export class OrganizationDetailsInfoCard implements OnInit, OnDestroy {
  /** The organization to show */
  @Input() organization?: Organization;
  /** The currently logged in user */
  @Input() profile?: Profile;
  isMember: boolean = false;
  members: any | undefined;
  showRequestButton: boolean = true;

  /** Holds data on whether or not the user is on a mobile device */
  public isHandset: boolean = false;
  private isHandsetSubscription!: Subscription;

  /** Holds data on whether or not the user is on a tablet */
  public isTablet: boolean = false;
  private isTabletSubscription!: Subscription;

  selectedTerm: string = '';

  /** Constructs the organization detail info card widget */
  constructor(
    private breakpointObserver: BreakpointObserver,
    private permission: PermissionService,
    protected snackBar: MatSnackBar,
    protected memberService: MemberService
  ) {}

  checkPermissions(): Observable<boolean> {
    return this.permission.check(
      'organization.update',
      `organization/${this.organization?.slug}`
    );
  }

  /** Runs whenever the view is rendered initally on the screen */
  isProfileInMembers: boolean = false;

  ngOnInit(): void {
    this.members = this.memberService.getAllMembers(
      this.organization!.slug,
      this.organization!.term
    );

    this.members.subscribe((members: any) => {
      // Check if profile.id exists in members
      this.isProfileInMembers = members.some(
        (member: { user: { id: number | null | undefined } }) =>
          member.user.id === this.profile?.id
      );
    });

    this.isHandsetSubscription = this.initHandset();
    this.isTabletSubscription = this.initTablet();
  }

  /** Unsubscribe from subscribers when the page is destroyed */
  ngOnDestroy(): void {
    this.isHandsetSubscription.unsubscribe();
    this.isTabletSubscription.unsubscribe();
  }

  requestMembership(profile: Profile) {
    this.memberService
      .addMember(this.organization!.slug, profile, this.organization!.term)
      .subscribe(
        (data) => {
          if (data.user) {
            this.snackBar.open(
              'Membership Requested for ' +
                data.user.first_name +
                ' ' +
                data.user.last_name +
                '!',
              undefined,
              { duration: 10000 }
            );
          }
          if (this.organization?.application) {
            this.snackBar.open('External Application Required', 'Close', {
              duration: 10000
            });
          }
          setTimeout(() => {
            window.location.reload();
          }, 5000);
        },
        (error) => {
          console.error(error);
          this.snackBar.open('Failed to request membership.', undefined, {
            duration: 10000
          });
        }
      );
  }

  onTermSelect(term: string): void {
    this.selectedTerm = term;
  }

  /** Determines whether the page is being used on a mobile device */
  private initHandset() {
    return this.breakpointObserver
      .observe([Breakpoints.Handset, Breakpoints.TabletPortrait])
      .pipe(map((result) => result.matches))
      .subscribe((isHandset) => (this.isHandset = isHandset));
  }

  /** Determines whether the page is being used on a tablet */
  private initTablet() {
    return this.breakpointObserver
      .observe(Breakpoints.TabletLandscape)
      .pipe(map((result) => result.matches))
      .subscribe((isTablet) => (this.isTablet = isTablet));
  }
}
