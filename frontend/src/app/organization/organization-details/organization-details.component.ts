/* eslint-disable @angular-eslint/use-lifecycle-interface */
/**
 * The Organization Detail Component displays more information and options regarding
 * UNC CS organizations.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route,
  TitleStrategy
} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { Organization } from '../organization.model';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
import {
  organizationDetailResolver,
  organizationEventsResolver
} from '../organization.resolver';
import { EventService } from 'src/app/event/event.service';
//changed
import { MemberService } from '../member-page/member.service';

import { Event } from 'src/app/event/event.model';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
//import { MemberRequestCardComponent } from '../widgets/member-request-card/member-request-card.component';

/** Injects the organization's name to adjust the title. */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['organization']?.name ?? 'Organization Not Found';
};

@Component({
  selector: 'app-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.css']
})
export class OrganizationDetailsComponent {
  /** Route information to be used in Organization Routing Module */
  slug: string | undefined;
  public static Route: Route = {
    path: ':slug',
    component: OrganizationDetailsComponent,
    resolve: {
      profile: profileResolver,
      organization: organizationDetailResolver,
      events: organizationEventsResolver,
      //changed
      members: organizationDetailResolver
    },
    children: [
      {
        path: '',
        title: titleResolver,
        component: OrganizationDetailsComponent
      }
    ]
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** The organization to show */
  public organization: Organization;

  /** Store a map of days to a list of events for that day */
  public eventsPerDay: [string, Event[]][];

  /** Whether or not the user has permission to update events. */
  public eventCreationPermission$: Observable<boolean>;
  memberDetails: any;

  /** Constructs the Organization Detail component */
  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    protected eventService: EventService,
    private permission: PermissionService,
    private memberService: MemberService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      organization: Organization;
      events: Event[];
      members: any[];
    };
    this.profile = data.profile;
    this.organization = data.organization;
    this.eventsPerDay = eventService.groupEventsByDate(data.events ?? []);
    this.eventCreationPermission$ = this.permission.check(
      'organization.events.*',
      `organization/${this.organization?.id ?? -1}`
    );
    this.memberDetails = data.members;
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      this.slug = params.get('slug')!;
      if (this.slug) {
        this.checkPermissions().subscribe((hasPermission) => {
          if (hasPermission) {
            this.fetchPendingMemberDetails();
          }
        });
      }
    });
  }

  fetchPendingMemberDetails(): void {
    this.memberService
      .getPendingMembers(this.slug!, this.organization.term)
      .subscribe({
        next: (data) => {
          this.memberDetails = data;
        },
        error: (error) => {
          console.error('Error fetching member details:', error);
        }
      });
  }

  checkPermissions(): Observable<boolean> {
    return this.permission.check('member.*', `organization/${this.slug}`);
  }
}
