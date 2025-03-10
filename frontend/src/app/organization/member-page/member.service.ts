import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Profile } from 'src/app/profile/profile.service';
import { MemberDetails } from './member_details.model';

@Injectable({
  providedIn: 'root'
})
export class MemberService {
  constructor(private http: HttpClient) {}

  getAllMembers(
    organizationName: string,
    term: string
  ): Observable<MemberDetails[]> {
    return this.http.get<MemberDetails[]>(
      `/api/organizations/${organizationName}/members/${term}`
    );
  }

  getApprovedMembers(
    organizationName: string,
    term: string
  ): Observable<MemberDetails[]> {
    return this.http.get<MemberDetails[]>(
      `/api/organizations/${organizationName}/members/${term}/approved`
    );
  }

  getLeaders(
    organizationName: string,
    term: string
  ): Observable<MemberDetails[]> {
    return this.http.get<MemberDetails[]>(
      `/api/organizations/${organizationName}/members/${term}/getLeaders`
    );
  }

  getPendingMembers(
    organizationName: string,
    term: string
  ): Observable<MemberDetails[]> {
    return this.http.get<MemberDetails[]>(
      `/api/organizations/${organizationName}/members/${term}/pending`
    );
  }

  addMember(
    slug: string,
    person: Profile,
    term: string
  ): Observable<MemberDetails> {
    return this.http.post<MemberDetails>(
      `/api/organizations/${slug}/members/${term}/${person.id}`,
      person
    );
  }

  adminStatus(
    slug: string,
    memberId: Number,
    term: string
  ): Observable<MemberDetails> {
    return this.http.put<MemberDetails>(
      `/api/organizations/${slug}/members/${term}/${memberId}/admin`,
      memberId
    );
  }

  removeAdmin(
    slug: string,
    memberId: Number,
    term: string
  ): Observable<MemberDetails> {
    return this.http.put<MemberDetails>(
      `/api/organizations/${slug}/members/${term}/${memberId}/removeAdmin`,
      memberId
    );
  }

  approveMember(
    slug: string,
    memberId: Number,
    term: string
  ): Observable<MemberDetails> {
    return this.http.put<MemberDetails>(
      `/api/organizations/${slug}/members/${term}/${memberId}/approved`,
      memberId
    );
  }

  getMemberById(
    slug: string,
    term: string,
    memberId: Number
  ): Observable<MemberDetails[]> {
    return this.http.get<MemberDetails[]>(
      `/api/organizations/${slug}/members/${term}/${memberId}/edit`
    );
  }

  deleteMember(
    slug: string,
    memberId: Number,
    term: string
  ): Observable<MemberDetails> {
    return this.http.delete<MemberDetails>(
      `/api/organizations/${slug}/members/${term}/${memberId}`
    );
  }

  makeLeader(
    slug: string,
    memberId: Number,
    term: string
  ): Observable<MemberDetails> {
    return this.http.put<MemberDetails>(
      `/api/organizations/${slug}/members/${term}/${memberId}/leader`,
      memberId
    );
  }

  removeLeader(
    slug: string,
    memberId: Number,
    term: string
  ): Observable<MemberDetails> {
    return this.http.put<MemberDetails>(
      `/api/organizations/${slug}/members/${term}/${memberId}/removeLeader`,
      memberId
    );
  }

  updateMember(slug: string, member: MemberDetails): Observable<MemberDetails> {
    return this.http.put<MemberDetails>(
      `/api/organizations/${slug}/members/{term}/{memberId}/edit`,
      member
    );
  }
}
