  #define BIG_ENDIAN      0
  #define LITTLE_ENDIAN   1

  int little_endian(void)
  {
      short int w = 0x0001;
      char *byte = (char *) &w;
      return(byte[0] ? LITTLE_ENDIAN : BIG_ENDIAN);
  }

main () {  
  if(little_endian()) {
     printf("-DSLM_SWAP_BYTES");
  } 
}
