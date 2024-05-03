APPNAME=myanimemanager3
APPVERSION=$(shell git show -s --format=%cd --date=format:"%Y.%m.%d")

FEDORA_VERSION=$(shell rpm -E %fedora)

archlinux-build:
	cd "packaging/PKGBUILD"; \
	rm -rf packaging/*.pkg.*; \
	makepkg --syncdeps --force --rmdeps --cleanbuild --clean; \
	rm -rf "MyAnimeManager 3"

archlinux-install:
	cd "packaging/PKGBUILD/dist"; \
	sudo pacman -U $(APPNAME)-$(APPVERSION)-* --noconfirm;

archlinux-build-install: archlinux-build archlinux-install

fedora-build:
	cd "packaging/rpm/"; \
	fedpkg --release f$(FEDORA_VERSION) local

fedora-install:

fedora-build-install: fedora-build fedora-install

windows-build:
	call packaging/windows/build.bat
