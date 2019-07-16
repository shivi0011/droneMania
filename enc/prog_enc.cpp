// ENCRYPTION_Video_streaming_9july2019.cpp : Defines the entry point for the console application.

#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include <math.h>

#define Quasigroup_order 256
using namespace std;
typedef long double ll;
class bbs {
	ll p, q, M, seed, actual;
	ll gcd(ll a, ll b)
	{
		if (b == 0)return a;
		return gcd(b, fmod(a, b));
	}

public:
	bbs(ll p, ll q, ll s) {
		this->p = p;
		this->q = q;
		this->seed = s;
		M = p*q;
		actual = s;
	}
	ll getrandom() {
		ll r = fmod(actual*actual, M);
		actual = r;
		return r;

	}
	ll getirandom(int i) {
		ll g = gcd(p, q);
		ll lcm = p*q / g;
		ll exp = 1;

		for (int j = 1; j <= i; ++j)exp = fmod((exp + exp), lcm);

		ll x0 = seed*seed;
		ll r = x0;
		for (int j = 2; j <= exp; ++j)r = fmod((r*x0), M);
		return r;
	}
};
void Q(unsigned char e[Quasigroup_order][Quasigroup_order])
{
	int i, j;
	for (i = 0; i<Quasigroup_order; i++)
	{
		for (j = 0; j<Quasigroup_order; j++)
		{
			if (i == 0)
				e[i][j] = (17 * i*j + 19 * j + 29) % Quasigroup_order;
			else
				e[i][j] = (e[i - 1][j] + i) % Quasigroup_order;
		}
	}
}
void Q256_get_left_parastrophe(unsigned char Q[][Quasigroup_order], unsigned char Q_par[][Quasigroup_order])
{
	int i, j;
	for (i = 0; i<Quasigroup_order; i++)
		for (j = 0; j<Quasigroup_order; j++)
			Q_par[i][Q[i][j]] = j;
}

int main(int argc, char *argv[])
{
	int scan = Quasigroup_order, pixel = 3 * Quasigroup_order*3, i, j, k, l;
	unsigned char *data = (unsigned char*)malloc((scan*pixel)*sizeof(unsigned char));
	unsigned char **org_img = (unsigned char**)malloc(scan*sizeof(unsigned char*));
	unsigned char **img_quasi = (unsigned char**)malloc(scan*sizeof(unsigned char*));
	unsigned char **img_quasirandom = (unsigned char**)malloc(scan*sizeof(unsigned char*));
	unsigned char **img_dequasi = (unsigned char**)malloc(scan*sizeof(unsigned char*));
	char filename[100];
	unsigned char *header;
	unsigned char e[Quasigroup_order][Quasigroup_order], e_par[Quasigroup_order][Quasigroup_order];

	printf("---scan = %d ----",scan);
	printf("--pixel = %d --- ",pixel);

	FILE *fp_original, *fp_quasi, *fp_quasirandom, *fp_derandom, *fp_dequasi;
	header = (unsigned char*)malloc(54 * sizeof(unsigned char));

	//	printf("\nprocessing over\n");
	if (argc<2)
	{
		fprintf(stderr, "usage%s bmpfilename\n", argv[0]);
	}
	//	printf("\nprocessing over\n");
	for (i = 0; i < scan; i++)
	{
		org_img[i] = (unsigned char*)malloc(pixel*sizeof(unsigned char));
		img_quasi[i] = (unsigned char*)malloc(pixel*sizeof(unsigned char));
		img_quasirandom[i] = (unsigned char*)malloc(pixel*sizeof(unsigned char));
		img_dequasi[i] = (unsigned char*)malloc(pixel*sizeof(unsigned char));
	}
	 strcpy(filename, argv[1]);
	if ((fp_original = fopen(filename, "rb")) == NULL)
	{
		printf("file does not exist");
	}
	if ((fp_quasi = fopen("file_quasi.bmp", "wb")) == NULL)
	{
		printf("quasified\file_quasi.bmp file does not exist");
	}
	if ((fp_dequasi = fopen("file_dequasi.bmp", "wb")) == NULL)
	{
		printf("file does not exist");
	}
	if ((fp_derandom = fopen("file_derandom.bmp", "wb")) == NULL)
	{
		printf("file does not exist");
	}
	if ((fp_quasirandom = fopen("file_quasirandom.bmp", "wb")) == NULL)
	{
		printf("file does not exist");
	}
	for (j = 0; j < 54; j++)
		fread(&header[j], sizeof(unsigned char), 1, fp_original);

	for (i = 0; i<scan; i++)
	{
		for (j = 0; j<(pixel); j++)
		{
			fread(&org_img[i][j], sizeof(unsigned char), 1, fp_original);
			 

		}
	}
	//	printf("\n1processing over\n");
	Q(e);
	for (i = 0; i<scan; )
	{
		for (j = 0; j<(pixel); )
		{
			for (k = 0; k<Quasigroup_order; k++)
			{
				for (l = 0; l<Quasigroup_order; l++)
				{
					img_quasi[i + k][j + e[k][l]] = org_img[i + k][j + l];
				}
			}
			j = j + Quasigroup_order;
		}
		i = i + Quasigroup_order;
	}

	//	printf("\nprocessing over\n");
	for (j = 0; j < 54; j++)
		fwrite(&header[j], sizeof(unsigned char), 1, fp_quasi);
	int linear = 0;
	for (i = 0; i<scan; i++)
	{
		for (j = 0; j<pixel; j++)
		{
			data[linear++] = img_quasi[i][j];
			fwrite(&img_quasi[i][j], sizeof(unsigned char), 1, fp_quasi);

		}
	}
	ll p = 87566873;
	ll q = 5631179;
	ll s = 191;
	ll M = 1;
	FILE *fp_bbs;
	//	ll digit;
	int nibbles[4], count = 0, index = 0;
	unsigned char quadret_0 = 0, quadret_1 = 0, *prng_bbs;
	if ((fp_bbs = fopen("bbs_output_bits_in_hexadecimal.txt", "wb")) == NULL)
		printf("file can't be opened\n");

	bbs b(p, q, s);
	int n = (Quasigroup_order*Quasigroup_order*3*3), count_n;
	prng_bbs = new unsigned char[n];
	printf("%d \n",n);    //cout << n << endl;
	count_n = 1;
	int llinear = 0;
	for (int i = 0; index<linear;)
	{
		for (int k = 0; k<4; k++)
		{


			if ((fmod(b.getrandom() / M, 2) == 0))
				nibbles[k] = 0;
			else
				nibbles[k] = 1;

		}
		if (count % 2 == 0)
			quadret_0 = 2 * 2 * 2 * nibbles[3] + 2 * 2 * nibbles[2] + 2 * nibbles[1] + nibbles[0];
		else if (count % 2 == 1)
		{
			quadret_1 = 2 * 2 * 2 * nibbles[3] + 2 * 2 * nibbles[2] + 2 * nibbles[1] + nibbles[0];

			prng_bbs[index] = (quadret_0 << 4) | (quadret_1);
			 	data[llinear] = data[llinear] ^ prng_bbs[index];
			fprintf(fp_bbs, "%02x", prng_bbs[index]);
			 	llinear++;

			index++;
			//	if (index == linear)index = 0;

		}
		if (i % 256 == 0)fprintf(fp_bbs, "\n");
		i = i + 4;
		count++;
		if (i >= n)
		{
			count_n++;
			i = 0;
		}

	}
/*	for (i = 0; i < linear; i++)
	{
		data[i] = data[i] ^ prng_bbs[i];
	}
*/	for (j = 0; j < 54; j++)
		fwrite(&header[j], sizeof(unsigned char), 1, fp_quasirandom);
	linear = 0;
	for (i = 0; i<scan; i++)
	{
		for (j = 0; j<pixel; j++)
		{
			img_quasirandom[i][j] = data[linear++];
			fwrite(&img_quasirandom[i][j], sizeof(unsigned char), 1, fp_quasirandom);

		}
	}
	for (i = 0; i < linear; i++)
	{
		data[i] = data[i] ^ prng_bbs[i];
	}
	linear = 0;
	for (i = 0; i<scan; i++)
	{
		for (j = 0; j<pixel; j++)
		{
			img_quasirandom[i][j] = data[linear++];


		}
	}
	for (j = 0; j < 54; j++)
		fwrite(&header[j], sizeof(unsigned char), 1, fp_derandom);

	for (i = 0; i<scan; i++)
	{
		for (j = 0; j<pixel; j++)
		{

			fwrite(&img_quasirandom[i][j], sizeof(unsigned char), 1, fp_derandom);

		}
	}
	Q256_get_left_parastrophe(e, e_par);
	for (i = 0; i<scan;)
	{
		for (j = 0; j<pixel;)
		{
			printf("j = %d",j);
			for (k = 0; k<Quasigroup_order; k++)
			{
				for (l = 0; l<Quasigroup_order; l++)
				{
					img_dequasi[i + k][j + e_par[k][l]] = img_quasirandom[i + k][j + l];

				}
			}
			j = j + Quasigroup_order;
		}
		i = i + Quasigroup_order;
	}



	for (j = 0; j < 54; j++)
	{
		fwrite(&header[j], sizeof(unsigned char), 1, fp_dequasi);

	}

	for (i = 0; i < scan; i++)
	{
		for (j = 0; j < pixel; j++)
		{
			fwrite(&img_dequasi[i][j], sizeof(unsigned char), 1, fp_dequasi);
		}
	}
	for (i = 0; i < scan; i++)
	{
		free(org_img[i]);
		free(img_quasi[i]);
		free(img_dequasi[i]);
		free(img_quasirandom[i]);
	}
	free(org_img);
	free(img_quasi);
	free(img_quasirandom);
	free(img_dequasi);
	free(prng_bbs);
	free(header);
	fclose(fp_original);
	fclose(fp_quasi);
	fclose(fp_dequasi);
	fclose(fp_derandom);
	fclose(fp_quasirandom);
	fclose(fp_bbs);
}