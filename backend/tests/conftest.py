import pytest
import os
import sys

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set required environment variables for testing
os.environ["NCBI_EMAIL"] = "test@example.com"
os.environ["NCBI_API_KEY"] = "test_key"
os.environ["SECRET_KEY"] = "test_secret"

from app.core.config import settings

@pytest.fixture
def mock_genome_file(tmp_path):
    """Create a mock GenBank file for testing."""
    d = tmp_path / "data"
    d.mkdir()
    p = d / "test_genome.gb"
    
    # Create a minimal GenBank file content
    content = """LOCUS       NC_000913               4641652 bp    DNA     circular BCT 01-JAN-2024
DEFINITION  Escherichia coli str. K-12 substr. MG1655, complete genome.
ACCESSION   NC_000913
VERSION     NC_000913.3
KEYWORDS    .
SOURCE      Escherichia coli str. K-12 substr. MG1655
  ORGANISM  Escherichia coli str. K-12 substr. MG1655
            Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales;
            Enterobacteriaceae; Escherichia.
FEATURES             Location/Qualifiers
     source          1..4641652
                     /organism="Escherichia coli str. K-12 substr. MG1655"
                     /mol_type="genomic DNA"
                     /strain="K-12"
                     /sub_strain="MG1655"
     CDS             190..255
                     /gene="thrL"
                     /locus_tag="b0001"
                     /function="leader; Amino acid biosynthesis: Threonine"
                     /product="thr operon leader peptide"
                     /translation="MKRISTTITTTITITTGNGAG"
ORIGIN
        1 agcttttcat tctgactgca acgggcaata tgtctctgtg tggattaaaa aaagagtgtc
       61 tgatagcagc ltctgaactg gttacctgcc gtgagtaaat taaaatttta ttgacttagg
      121 tcactaaata ctttaaccaa tataggcata gcgcacagac agataaaaat tacagagtac
      181 acaacatcca tgaaacgcat tagcaccacc attaccacca ccatcaccat taccacaggt
      241 aacggtgcgg gctgacgcgt acaggaaaca cagaaaaaag cccgcacctg acagtgcggg
      301 cttttttttc gaccaaagg t aacgaggtaa caaccatgcg agtgttgaag ttcggcggta
//
"""
    p.write_text(content)
    return str(p)
