import sys
import subprocess
from csv import DictReader


# Nomeclatura
# fpath, fname, fhand
# fpath : direccion absoluta
# fname: nombre del archivo
# fhand : archivo en memoria


def ejemplo_subprocess(fpath):
	command_to_run = ["cut", "-f1", fpath]
	stdout = subprocess.check_output(command_to_run)
	print(stdout)
	print(stdout.decode())



def get_squared_number(num):
	num_squared = num**2
	return num_squared



# def get_gRNA_features(gRNA_fhand):
# 	grna_features = {gRNA: {seq: secuencia, efficiency: eficiencia}}
# 	return grna_features


# def get_grna_matches_in_genome(grna_features, refence_genome_fpath):
# 	return grna_matches

# def generate_bed_from_matches(grna_matches):
# 	return bed 

# def write_bed_into_file(bed, out_bed_fhand):


def test():
    assert get_squared_number(2) == 4
    assert get_squared_number(3) != 3
    assert get_squared_number(3) == 9
    assert True

# esto para probar las cosas 
def test_blast_parser():
	grna_features = {} # diccionario con los gRNA del csv
	genome_fpath = '' # la direccion del genoma
	blast_results = get_grna_matches_in_genome(grna_features, genome_fpath) 
	assert len(blast_results) == 21 
	blast_results_filtered = filter_blast_results # funcion que tengo que escribir, filtra si tiene 100% identeidad y 15 nts de longitud
	assert len(blast_results_filtered) == 2

def main():

	fpath = '/home/andres/Desktop/practicas/test_data/testgRNAs.csv'
	ejemplo = ejemplo_subprocess(fpath)
	
# do_test = False
# if do_test:
# 	test()
# else:
# 	num = int(sys.argv[1])
# 	print(get_squared_number(num))
# 	fpath = sys.argv[2]
# 	ejemplo_subprocess(fpath)



if __name__ == '__main__':
 	main()
	
