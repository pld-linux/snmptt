# TODO:
# - chkconfig in pre/post
# - separate package with init script and handler
%include	/usr/lib/rpm/macros.perl
Summary:	An SNMP trap handler for use with NET-SNMP/UCD-SNMP
Name:		snmptt
Version:	0.9
Release:	0.1
License:	GPL v2
Group:		Networking
Source0:	http://dl.sourceforge.net/snmptt/%{name}_%{version}.tgz
# Source0-md5:	85090dee54ed5772c4e6ec939d954271
Source1:	%{name}.init
URL:		http://www.snmptt.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SNMPTT is an SNMP trap handler written in Perl for use with the
NET-SNMP/UCD-SNMP snmptrapd program. Received traps are translated
into friendly messages using variable substitution. Output can be to
STDOUT, text log file, syslog, NT Event Log, MySQL (Linux/Windows),
PostgreSQL, or an ODBC database. User defined programs can also be
executed.

%prep
%setup -q -n %{name}_%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/{snmp,rc.d/init.d}}

install snmptt $RPM_BUILD_ROOT%{_sbindir}
install snmptthandler $RPM_BUILD_ROOT%{_sbindir}
install snmptt.ini $RPM_BUILD_ROOT%{_sysconfdir}/snmp/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog README examples docs
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/snmp/snmptt.ini
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /etc/rc.d/init.d/%{name}
