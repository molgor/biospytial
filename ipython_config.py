#!/usr/bin/env python
#-*- coding: utf-8 -*-
# ipython_config.py

c = get_config()

# Allow all IP addresses to use the service and run it on port 80.
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888

# Don't load the browser on startup.
c.NotebookApp.open_browser = False

#c.TerminalIPythonApp.display_banner = False 


c.TerminalInteractiveShell.banner1 = u"""

=========================================================================
Welcome to : 

██████╗ ██╗ ██████╗ ███████╗██████╗ ██╗   ██╗████████╗██╗ █████╗ ██╗     
██╔══██╗██║██╔═══██╗██╔════╝██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║██╔══██╗██║     
██████╔╝██║██║   ██║███████╗██████╔╝ ╚████╔╝    ██║   ██║███████║██║     
██╔══██╗██║██║   ██║╚════██║██╔═══╝   ╚██╔╝     ██║   ██║██╔══██║██║     
██████╔╝██║╚██████╔╝███████║██║        ██║      ██║   ██║██║  ██║███████╗
╚═════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝        ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═╝╚══════╝                                                                                                                                           
                                                        -(2.C.I. 2017)-   
                                                        
A multipurpose opensource framework for modelling biodiversity in Earth                                                                                                                                                                                                                                            
----------------------------------------------------------------------------

Copyright: Juan M. Escamilla Mólgora 
           http://juan.escamilla.holobio.me
           j.escamillamolgora@lancaster.ac.uk
           molgor@gmail.com
        
Docs    : test.holobio.me   
@docker : https://hub.docker.com/r/molgor/biospytial/
@github : https://github.com/molgor/biospytial

Funded by: CONACYT (Mexico), Lancaster University (U.K), GBIF (Int.)          


"""

c.TerminalInteractiveShell.banner2 = """
   |             
   |.===.        
   {}o o{}       
ooO--(_)--Ooo-------------------------------------------------------
This console is based on IPython 5.1.0 
Type \"copyright\", \"credits\" or \"license\" for more information
====================================================================

"""