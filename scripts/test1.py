import sys
import subprocess
import tempfile
from csv import DictReader
# from fastnumbers import fast_forceintfast_forceint  # esto para hacer int el 100.000 que si no no me dejas

# def get_gRNA_features(gRNA_fhand):
# 	grna_features = {gRNA: {seq: secuencia, efficiency: eficiencia}}
# 	return grna_features

# def get_grna_matches_in_genome(grna_features, refence_genome_fpath):
# 	return grna_matches

# def generate_bed_from_matches(grna_matches):
# 	return bed 

# def write_bed_into_file(bed, out_bed_fhand):


# la cosa que hay gRNAs que se usan para mas de un gen
def get_gRNA_features(gRNA_fhand):
    gRNA_features = {}
    header = gRNA_fhand.readline() 
    for line in gRNA_fhand:
        line = line.rstrip()
        fields = line.split()
        gRNA = fields[0]
        seq = fields[1]
        target_gene = fields[2]
        efficiency = fields[3]

        if gRNA not in gRNA_features:
            gRNA_features[gRNA] = {'seq':seq, 'target_genes':{target_gene:{'efficiency':efficiency}}}
        
        elif gRNA in gRNA_features:
            diccionario_gRNAs = gRNA_features[gRNA]
            diccionario_target_genes = diccionario_gRNAs['target_genes']
            diccionario_target_genes[target_gene] = {'efficiency':efficiency}
        
    return(gRNA_features)


def make_gRNA_fasta_file(gRNA_features):
    gRNA_fasta_fhand = tempfile.NamedTemporaryFile()
    for key in gRNA_features.keys():
        gRNA_sequence = '>' + key + '\n' + gRNA_features[key]['seq'] + '\n'
        gRNA_fasta_fhand.write(gRNA_sequence.encode('utf-8'))
        gRNA_fasta_fhand.flush()

    return(gRNA_fasta_fhand)


def get_gRNA_matches_in_genome(gRNA_fasta_fhand, reference_genome_fpath):
    gRNA_matches = ['blastn', '-query', gRNA_fasta_fhand.name, '-db', 
                    reference_genome_fpath, '-task',
                    'blastn-short', '-outfmt', '6']

    stdout = subprocess.check_output(gRNA_matches).decode('utf-8').split('\n')
    #print('\n'.join(stdout))
    gRNA_fasta_fhand.close() # con esto el archivo deja de existir

    return(stdout)
    

def filter_blast_matches(gRNA_matches, identity=100, aln_length=15):
    filtered_gRNA_matches = [] 
    for line in gRNA_matches:
        if line: # si hay una linea vacia es como si hay '' y es falso
            line = line.rstrip()
            fields = line.split()
            match_identity = float(fields[2]) 
            match_aln_length = int(fields[3])
        
            if match_identity >= identity and match_aln_length >= aln_length:
                filtered_gRNA_matches.append(line)

    return(filtered_gRNA_matches)


def create_bed_lines(filtered_gRNA_matches): # PORQUEEE NO VAAA
    bed_lines = []
    for line in filtered_gRNA_matches:
        fields = line.split()
        query_name = fields[0]
        subject_name = fields[1]
        subject_start = fields[9]
        subject_end = fields[10]
        score = fields[11]

        if int(subject_start) > int(subject_end):
            bed_lines.append(subject_name + '\t' + subject_start + '\t'
                            + subject_end + '\t' + query_name + '\t'
                            + score + '\t +\n')
        
        elif int(subject_start) < int(subject_end):
            bed_lines.append(subject_name + '\t' + subject_start + '\t'
                            + subject_end + '\t' + query_name + '\t'
                            + score + '\t -\n')
    print(bed_lines)
    return(bed_lines)


def write_bed_file(bed_lines, bed_file):
    for line in bed_lines:
        bed_file.write(line)
    
    return(bed_file)


# los test van todos juntos abajo
def test_gRNA_matches_in_genome(): # dentro del test es donde defino las variables
    gRNA_fhand = open('/home/andres/Desktop/practicas/test_data/testgRNAs.fasta') # dentro van hard coded las variables
    reference_genome_fpath = '/home/andres/Desktop/practicas/test_data/testchrom.fasta'
    gRNA_matches = get_gRNA_matches_in_genome(gRNA_fhand, reference_genome_fpath)
    assert len(gRNA_matches) == 22


def test_filter_blast_matches():
    gRNA_fhand = open('/home/andres/Desktop/practicas/test_data/testgRNAs.fasta')
    reference_genome_fpath = '/home/andres/Desktop/practicas/test_data/testchrom.fasta'
    gRNA_matches = get_gRNA_matches_in_genome(gRNA_fhand, reference_genome_fpath)
    filtered_gRNA_matches = filter_blast_matches(gRNA_matches)
    assert len(filtered_gRNA_matches) == 2



def main():
    do_test = True # esto si lo pongo True hara el do_test
    if do_test:
        test_gRNA_matches_in_genome()
        test_filter_blast_matches()
    else:
        gRNA_fhand = open(sys.argv[1])
        bed_file = open(sys.argv[2],'w')
        reference_genome_fpath = '/home/andres/Desktop/practicas/test_data/testchrom.fasta'
        gRNA_features = get_gRNA_features(gRNA_fhand)
        gRNA_seqs = make_gRNA_fasta_file(gRNA_features)
        gRNA_matches = get_gRNA_matches_in_genome(gRNA_seqs, reference_genome_fpath)
        filtered_gRNA_matches = filter_blast_matches(gRNA_matches)
        bed_lines = create_bed_lines(filtered_gRNA_matches)
        write_bed_file(bed_lines, bed_file)
        #create_bed_from_matches(gRNA_fhand, filtered_gRNA_matches)


if __name__ == '__main__':
 	main()
    