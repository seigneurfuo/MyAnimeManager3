%define version %(git show -s --format=%cd --date=format:"%Y.%m.%d")
%define src_root %(realpath $PWD)

Name:           myanimemanager3
Version:        %{version}
Release:        %autorelease
BuildArch:      noarch
Summary:        Un logiciel de gestion de séries et d'animés.

License:        None
URL:            https://seigneurfuo.com

Requires:       python3-PyQt6
Requires:       python3-peewee

%description
Un logiciel de gestion de séries et d'animés.

%install

# ./
mkdir -p %{buildroot}/opt/%{name}
cp %{src_root}/../../src/*.py %{buildroot}/opt/%{name}/

# Patching Version
sed -i "s/\"DEV\"/\"%{version}\"/g" "%{buildroot}/opt/%{name}/core.py"

# ./resources/
mkdir -p %{buildroot}/opt/%{name}/resources
cp %{src_root}/../../src/resources/icon.png %{buildroot}/opt/%{name}/resources/

# ./resources/icons/
mkdir -p %{buildroot}/opt/%{name}/resources/icons
cp %{src_root}/../../src/resources/icons/*.png %{buildroot}/opt/%{name}/resources/icons/

# ./ui/
mkdir -p %{buildroot}/opt/%{name}/ui/
cp %{src_root}/../../src/ui/*.py %{buildroot}/opt/%{name}/ui/
cp %{src_root}/../../src/ui/*.ui %{buildroot}/opt/%{name}/ui/

# ./ui/dialogs/
mkdir -p %{buildroot}/opt/%{name}/ui/dialogs
cp %{src_root}/../../src/ui/dialogs/*.py %{buildroot}/opt/%{name}/ui/dialogs/
cp %{src_root}/../../src/ui/dialogs/*.ui %{buildroot}/opt/%{name}/ui/dialogs/

# ./ui/tabs/
mkdir -p %{buildroot}/opt/%{name}/ui/tabs
cp %{src_root}/../../src/ui/tabs/*.py %{buildroot}/opt/%{name}/ui/tabs/
cp %{src_root}/../../src/ui/tabs/*.ui %{buildroot}/opt/%{name}/ui/tabs/

# ./ui/widgets/
mkdir -p %{buildroot}/opt/%{name}/ui/widgets
cp %{src_root}/../../src/ui/widgets/*.py %{buildroot}/opt/%{name}/ui/widgets/

# Racourcis d'applciation
mkdir -p %{buildroot}/usr/share/applications/
cp %{src_root}/myanimemanager3.desktop %{buildroot}/usr/share/applications/myanimemanager3.desktop

# Permissions

%files
# ./
/opt/%{name}/*.py

# ./resources/
/opt/%{name}/resources/icon.png

# ./resources/icons/
/opt/%{name}/resources/icons/*.png

# ./ui/
/opt/%{name}/ui/*.py
/opt/%{name}/ui/*.ui

# ./ui/dialogs/
/opt/%{name}/ui/dialogs/*.py
/opt/%{name}/ui/dialogs/*.ui

# ./ui/tabs/
/opt/%{name}/ui/tabs/*.py
/opt/%{name}/ui/tabs/*.ui

# ./ui/widgets/
/opt/%{name}/ui/widgets/*.py

# ./usr/share/applicationss
/usr/share/applications/myanimemanager3.desktop
