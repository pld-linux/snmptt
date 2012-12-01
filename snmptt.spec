# TODO:
# - logrotate file
#
%include	/usr/lib/rpm/macros.perl
Summary:	An SNMP trap handler for use with NET-SNMP/UCD-SNMP
Summary(pl.UTF-8):	Program do obsługi pułapek SNMP do używania z NET-SNMP/UCD-SNMP
Name:		snmptt
Version:	1.3
Release:	1
License:	GPL v2
Group:		Networking
Source0:	http://dl.sourceforge.net/snmptt/%{name}_%{version}.tgz
# Source0-md5:	ee8d8206d3e0d860fee126e09d8eb207
Source1:	%{name}.init
URL:		http://www.snmptt.org/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	rpm-perlprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SNMPTT is an SNMP trap handler written in Perl for use with the
NET-SNMP/UCD-SNMP snmptrapd program. Received traps are translated
into friendly messages using variable substitution. Output can be to
STDOUT, text log file, syslog, NT Event Log, MySQL (Linux/Windows),
PostgreSQL, or an ODBC database. User defined programs can also be
executed.

%description -l pl.UTF-8
SNMPTT to program obsługujący pułapki SNMP napisany w Perlu, do
używania z programem snmptrapd z pakietu NET-SNMP/UCD-SNMP. Otrzymane
pułapki są tłumaczone na przyjazne komunikaty przez podstawienia
zmiennych. Wyjściem może być STDOUT, plik loga tekstowego, syslog,
Event Log NT, MySQL (Linux/Windows), PostgreSQL albo baza danych ODBC.
Można także wywoływać zdefiniowane przez użytkownika programy.

%package init
Summary:	An SNMP trap handler for use with NET-SNMP/UCD-SNMP - daemon script
Summary(pl.UTF-8):	Program do obsługi pułapek SNMP do używania z NET-SNMP/UCD-SNMP - skrypt demona
Group:		Networking/Daemons
Provides:	user(snmptt)
Provides:	group(snmptt)
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):  /bin/id
Requires(pre):  /usr/sbin/useradd
Requires(pre):  /usr/bin/getgid
Requires(pre):  /usr/sbin/groupadd
Requires(pre):	/usr/lib/rpm/user_group.sh
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/usermod
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description init
Init scripts for SNMPTT.

%description init -l pl.UTF-8
Skrypt init dla SNMPTT.

%prep
%setup -q -n %{name}_%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/snmp} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/log,/var/spool/snmptt}

install snmptt $RPM_BUILD_ROOT%{_sbindir}
install snmptthandler $RPM_BUILD_ROOT%{_sbindir}
install snmptt.ini $RPM_BUILD_ROOT%{_sysconfdir}/snmp
install examples/snmptt.conf.generic $RPM_BUILD_ROOT%{_sysconfdir}/snmp/snmptt.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

touch $RPM_BUILD_ROOT/var/log/{snmptt.{log,debug},snmpttunknown.log}

%clean
rm -rf $RPM_BUILD_ROOT

%pre init
%groupadd -g 285 snmptt
%useradd -u 285 -c 'SNMPTT' -g snmptt snmptt

%post init
/sbin/chkconfig --add %{name}
%service snmptt restart

%preun init
if [ "$1" = "0" ]; then
	%service snmptt stop
	/sbin/chkconfig --del snmptt
fi

%postun init
if [ "$1" = "0" ]; then
	%userremove snmptt
	%groupremove snmptt
fi

%triggerin init -- nagios
# so SNMPTT can be used to post nagios commands
%addusertogroup -q snmptt nagcmd

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog README examples docs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/snmp/snmptt.ini
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/snmp/snmptt.conf
%attr(755,root,root) %{_sbindir}/snmptt
%config(noreplace) %verify(not md5 mtime size) /var/log/*.log
%config(noreplace) %verify(not md5 mtime size) /var/log/*.debug

%files init
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/snmptthandler
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(771,root,snmptt) /var/spool/snmptt
