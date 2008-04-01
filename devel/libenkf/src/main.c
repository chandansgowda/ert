#include <enkf_fs.h>
#include <enkf_main.h>
#include <enkf_config.h>
#include <enkf_site_config.h>
#include <util.h>
#include <basic_queue_driver.h>
#include <plain_driver.h>
#include <plain_driver_static.h>
#include <plain_driver_parameter.h>
#include <config.h>
#include <hash.h>
#include <fs_index.h>
#include <enkf_types.h>
#include <string.h>
#include <local_driver.h>
#include <lsf_driver.h>


int main (int argc , char ** argv) {
  const char * site_config_file = SITE_CONFIG_FILE;  /* The variable SITE_CONFIG_FILE should be defined on compilation ... */
  const char * config_file      = "Config/enkf";
  
  ecl_queue_type   * ecl_queue;
  enkf_main_type   * enkf_main;
  enkf_site_config_type * site_config = enkf_site_config_bootstrap(site_config_file);
  enkf_config_type * enkf_config      = enkf_config_fscanf_alloc(config_file , site_config , 1 , false , false , true);

  plain_driver_type * dynamic_analyzed 	      = plain_driver_alloc(enkf_config_get_ens_path(enkf_config) 	   , "%04d/mem%03d/Analyzed");
  plain_driver_type * dynamic_forecast 	      = plain_driver_alloc(enkf_config_get_ens_path(enkf_config) 	   , "%04d/mem%03d/Forecast");
  plain_driver_parameter_type * parameter     = plain_driver_parameter_alloc(enkf_config_get_ens_path(enkf_config) , "%04d/mem%03d/Parameter");
  plain_driver_static_type * eclipse_static   = plain_driver_static_alloc(enkf_config_get_ens_path(enkf_config)    , "%04d/mem%03d/Static");
  fs_index_type     * fs_index                = fs_index_alloc(enkf_config_get_ens_path(enkf_config) , "INDEX/mem%03d/INDEX");
  enkf_fs_type     * fs = enkf_fs_alloc(fs_index , dynamic_analyzed, dynamic_forecast , eclipse_static , parameter);
  
  ecl_queue = enkf_config_alloc_ecl_queue(enkf_config , site_config);
  enkf_main = enkf_main_alloc(enkf_config , fs , ecl_queue);
  enkf_main_run(enkf_main , 0 , 3);
  

  /*
    enkf_main_analysis(enkf_main);
    enkf_main_add_data_kw(enkf_main , "INIT" , "INCLUDE\n  \'EQUIL.INC\'/\n");
    enkf_main_init_eclipse(enkf_main);
  */
  
  enkf_config_free(enkf_config);
  enkf_main_free(enkf_main);
  enkf_fs_free(fs);
}
