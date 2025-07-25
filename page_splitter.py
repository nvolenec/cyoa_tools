import argparse
import re
import string
import calc_ioc

def process_args():
    parser = argparse.ArgumentParser( prog='page_splitter',
                                      description='splits cyoa book by pages' )
    parser.add_argument( 'book' )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = process_args()
    with open( args.book, 'r' ) as f:
        book = f.read().lower()
    pages = re.split( r'(page ?\d+)', book, flags=re.IGNORECASE )
    #print( pages )

    unknown_c = 1
    c=1
    while c < len( pages ):
        c0_match = re.search( r'page? \d+', pages[c-1], flags=re.IGNORECASE )
        c1_match = re.search( r'page? \d+', pages[c], flags=re.IGNORECASE ) 
        #print( str(c-1)+':  \''+pages[c-1][:30]+'\'    '+str(c0_match) )
        #print( str(c)+':  \''+pages[c][:30]+'\'    '+str(c1_match) )
        if c0_match and c1_match:
            #both match page * so just skip both
            c += 2
            #print( '   case 1' )
        if c1_match:
            splits = pages[c].split()
            #print( splits )
            pagenum = str(splits[1])
            if len(pages[c-1]) > sum(1 for char in pages[c-1] if char in string.whitespace):
                if int(splits[1]) < 10:
                    pagenum = '0'+str(splits[1])
                with open( 'page'+pagenum+'.txt', 'w' ) as f:
                    f.write(pages[c-1])
                print( 'page'+pagenum+' IOC = '+str(calc_ioc.index_of_coincidence(pages[c-1])) )
            #print( '    outputting page'+pagenum )
            #print( '   case 2' )
            c += 2
        elif c0_match:
            #print( '   case 3' )
            c += 1
        else:
            pagenum = str(unknown_c)
            if unknown_c < 10:
                pagenum = '0'+str(unknown_c)
            #if len(pages[c-1]):
            print( 'page'+pagenum+'    '+str(len(pages[c-1])))
            with open( 'unkwn_page'+pagenum+'.txt', 'w' ) as f:
                f.write(pages[c-1])
            #print( '    outputting unkwn_page'+pagenum )
            #print( '   case 4' )
            c += 1
            unknown_c += 1
    
