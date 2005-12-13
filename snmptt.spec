# TODO:
# - spooldir for daemon mode: /var/spool/snmptt/
# - logrotate file
#
%include	/usr/lib/rpm/macros.perl
Summary:	An SNMP trap handler for use with NET-SNMP/UCD-SNMP
Summary(pl):	Program do obs³ugi pu³apek SNMP do u¿ywania z NET-SNMP/UCD-SNMP
Name:		snmptt
Version:	1.0
Release:	1
License:	GPL v2
Group:		Networking
Source0:	http://dl.sourceforge.net/snmptt/%{name}_%{version}.tgz
# Source0-md5:	ad93fc3d7b28eb59c153ce2761644838
Source1:	%{name}.init
URL:		http://www.snmptt.org/
BuildRequires:	rpm-perlprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SNMPTT is an SNMP trap handler written in Perl for use with the
NET-SNMP/UCD-SNMP snmptrapd program. Received traps are translated
into friendly messages using variable substitution. Output can be to
STDOUT, text log file, syslog, NT Event Log, MySQL (Linux/Windows),
PostgreSQL, or an ODBC database. User defined programs can also be
executed.

%description -l pl
SNMPTT to program obs³uguj±cy pu³apki SNMP napisany w Perlu, do
u¿ywania z programem snmptrapd z pakietu NET-SNMP/UCD-SNMP. Otrzymane
pu³apki s± t³umaczone na przyjazne komunikaty przez podstawienia
zmiennych. Wyj¶ciem mo¿e byæ STDOUT, plik loga tekstowego, syslog,
Event Log NT, MySQL (Linux/Windows), PostgreSQL albo baza danych ODBC.
Mo¿na tak¿e wywo³ywaæ zdefiniowane przez u¿ytkownika programy.

%package init
Summary:	An SNMP trap handler for use with NET-SNMP/UCD-SNMP - daemon script
Summary(pl):	Program do obs³ugi pu³apek SNMP do u¿ywania z NET-SNMP/UCD-SNMP - skrypt demona
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description init
Init scripts for SNMPTT.

%description init -l pl
Skrypt init dla SNMPTT.

%prep
%setup -q -n %{name}_%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/snmp,/etc/rc.d/init.d,/var/log}

install snmptt $RPM_BUILD_ROOT%{_sbindir}
install snmptthandler $RPM_BUILD_ROOT%{_sbindir}
install snmptt.ini $RPM_BUILD_ROOT%{_sysconfdir}/snmp
install examples/snmptt.conf.generic $RPM_BUILD_ROOT%{_sysconfdir}/snmp/snmptt.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

touch $RPM_BUILD_ROOT/var/log/{snmptt.{log,debug},snmpttunknown.log}

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} service."
fi

%preun init
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop
	fi
	/sbin/chkconfig --del
fi

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
