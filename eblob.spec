Summary:	Append-only low-level IO library, which saves data in blob files
Name:		eblob
Version:	0.23.13
Release:	2%{?dist}

License:	GPLv2+
URL:		http://reverbrain.com/eblob
Source0:	https://github.com/reverbrain/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:		eblob-0.23.13-libversioning.patch

BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	python-devel
BuildRequires:	handystats-devel >= 1.10.2


%description
libeblob is a low-level IO library which stores data in huge blob files
appending records one after another.

    * fast append-only updates which do not require disk seeks
    * compact index to populate lookup information from disk
    * multi-threaded index reading during starup
    * O(1) data location lookup time
    * ability to lock in-memory lookup index (hash table) to eliminate
	memory swap
    * readahead games with data and index blobs for maximum performance
    * multiple blob files support (tested with blob-file-as-block-device too)
    * optional sha256 on-disk checksumming
    * 2-stage write: prepare (which reserves the space) and commit
	(which calculates checksum and update in-memory and on-disk indexes).
	One can (re)write data using pwrite() in between without locks
    * usuall 1-stage write interface
    * flexible configuration of hash table size, flags, alignment
    * defragmentation tool: entries to be deleted are only marked as removed,
	eblob_check will iterate over specified blob files and actually
	remove those blocks
    * off-line blob consistency checker: eblob_check can verify checksums
	for all records which have them
    * run-time sync support - dedicated thread runs fsync on all files
	on timed base
    * in-memory index lives in memory mapped file

%package libs
Summary:	Libraries for %{name}


%description libs
Eblob is a low-level IO library which stores data in huge blob files
appending records one after another.

This packae contains %{name} libraries

%package devel
Summary:	Development package for %{name}
Requires:	%{name}-libs%{_isa} = %{version}-%{release}


%description devel
Eblob is a low-level IO library which stores data in huge blob files
appending records one after another.

This package contains header files and developer documentation
needed for developing software which uses the eblob library.

%prep
%autosetup -p 1 

%build
%{cmake} .
make %{?_smp_mflags}

%install
%{make_install}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%license LICENSE
%doc AUTHORS README.rst
%{_bindir}/%{name}_index_info
%{_bindir}/%{name}_merge
%{_bindir}/%{name}_to_index

%files libs
%doc AUTHORS README.rst
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}_cpp.so.*
%{_libdir}/lib%{name}_python.so.*

%files devel
%doc AUTHORS README.rst
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_cpp.so
%{_libdir}/lib%{name}_python.so

%changelog
* Thu Jan 26 2017 Arkady L. Shane <ashejn@russianfedora.pro> - 0.23.13-2
- drop exclusivearch
* Tue Jan 10 2017 Arkady L. Shane <ashejn@russianfedora.pro> - 0.23.13-1
- initial build
