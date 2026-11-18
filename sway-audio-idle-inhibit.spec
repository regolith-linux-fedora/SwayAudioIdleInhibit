Name:           sway-audio-idle-inhibit
Version:        2.0.1
Release:        1%{?dist}
Summary:        Inhibit idle while audio is playing or recording
# LICENSE is the GPL version 3 text and no source file states a version;
# debian/copyright says GPL-3.0+.
License:        GPL-3.0-only
URL:            https://github.com/regolith-linux/SwayAudioIdleInhibit
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(libpulse) >= 15.0
BuildRequires:  pkgconfig(libsystemd)

%description
Takes an idle inhibitor lock from the login manager while any
application plays or records audio through PulseAudio or PipeWire's pulse
server, so that idle handling which respects these locks does not blank,
lock or suspend. It can also print whether audio is playing or recording.

%prep
%autosetup

%build
%meson -Dlogind-provider=systemd
%meson_build

%install
%meson_install
# Debian's postinst (dh_installsystemduser) enables the user unit for every
# user, in graphical-session.target.wants. A user preset does the same through
# %%systemd_user_post. The unit itself only starts in the Regolith Wayland
# session (ConditionEnvironment).
install -d %{buildroot}%{_userpresetdir}
echo "enable %{name}.service" > %{buildroot}%{_userpresetdir}/90-%{name}.preset

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service
%{_userpresetdir}/90-%{name}.preset

%changelog
* Wed Nov 18 2026 Regolith Fedora Port <port@regolith.invalid> - 2.0.1-1
- Initial package
