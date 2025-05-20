def calculate_skkm_point(kategori: str, capaian: str, tingkat: str) -> int:
    """
    Menghitung poin SKKM berdasarkan parameter
    """
    point_map = {
        'akademik': {
            'lokal': {'juara 1': 30, 'juara 2': 25, 'juara 3': 20, 'peserta': 10},
            'nasional': {'juara 1': 50, 'juara 2': 40, 'juara 3': 30, 'peserta': 20},
            'internasional': {'juara 1': 100, 'juara 2': 80, 'juara 3': 60, 'peserta': 40}
        },
        'non-akademik': {
            'lokal': {'juara 1': 20, 'juara 2': 15, 'juara 3': 10, 'peserta': 5},
            'nasional': {'juara 1': 40, 'juara 2': 30, 'juara 3': 20, 'peserta': 10},
            'internasional': {'juara 1': 80, 'juara 2': 60, 'juara 3': 40, 'peserta': 20}
        }
    }
    
    try:
        return point_map[kategori][tingkat][capaian]
    except KeyError:
        return 0
