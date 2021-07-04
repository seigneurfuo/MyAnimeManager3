dist-archlinux:
	cd "dist/PKGBUILD"; \
	makepkg  --syncdeps --force --rmdeps --cleanbuild --clean; \
	rm -rf "MyAnimeManager 3"

dist-manjaro:
	dist-archlinux

dist:
	dist-archlinux;
