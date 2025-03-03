/* -------------------------------------------------------------------------------------
 * Copyright 2012 EPFL-I&C-LCA
 *
 * Designed and Developed by: Vincent Bindschaedler and Reza Shokri
 *
 * Authors: Reza Shokri, George Theodorakopoulos, Vincent Bindschaedler, George Danezis, 
 *          Jean-Pierre Hubaux, Jean-Yves Le Boudec
 * 
 * Contact: reza.shokri@epfl.ch
 *
 * Redistribution and use in source and binary forms, with or without modification, 
 * are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this 
 *    list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice, 
 *    this list of conditions and the following disclaimer in the documentation 
 *    and/or other materials provided with the distribution.
 * 3. The name of the authors/developers may not be used to endorse or promote 
 *    products derived from this software without specific prior written permission.
 * 4. All advertising materials and/or any publications mentioning features or use of 
 *    this software must acknowledge it by citing the followings:
 *    [a] Location-Privacy Meter: A Tool to Quantify Location Privacy. 
 *        Available at http://lca.epfl.ch/projects/quantifyingprivacy/
 *    [b] Reza Shokri, George Theodorakopoulos, Jean-Yves Le Boudec, and Jean-Pierre 
 *        Hubaux. Quantifying Location Privacy. In IEEE Symposium on Security and 
 *        Privacy (S&P), Oakland, CA, USA, May 22-25, 2011.
 *    [c] Reza Shokri, George Theodorakopoulos, George Danezis, Jean-Pierre Hubaux, 
 *        and Jean-Yves Le Boudec. Quantifying Location Privacy: The Case of Sporadic
 *        Location Exposure. In The 11th Privacy Enhancing Technologies Symposium 
 *        (PETS), Waterloo, Canada, July 27-29, 2011.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
 * AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
 * ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * -------------------------------------------------------------------------------------
 */
#ifndef LPM_OPERATIONS_H
#define LPM_OPERATIONS_H

//!
//! \file
//!
#include <string>
using namespace std;
#include "Reference.h"

#include "Defs.h"

namespace lpm {

//!
//! \brief Abstract base class for all operations.
//!
//! Abstract template base class from which all operations classes derive. 
//! The two template parameters represent the input and output object types, respectively.
//!
template<typename InputType, typename OutputType>
class Operation : public Reference<Operation<InputType, OutputType> > 
{
  protected:
    string operationName;


  public:
    explicit Operation(string name);

    virtual ~Operation();

    //! 
    //! \brief Execute the operation
    //!
    //! Pure virtual method which executes the operation. 
    //!
    //! \tparam[[in] input 	InputType* to the input object of the operation.
    //! \tparam[[in,out] output 	OutputType* to the output object of the operation.
    //!
    //! \return true if the operation is successful, false otherwise
    //!
    virtual bool Execute(const InputType* input, OutputType* output) = 0;

    //! 
    //! \brief Gets a detailed string of the operation
    //!
    //! \return a string detailing the operation
    //!
    virtual string GetDetailString() = 0;

};
template<typename InputType, typename OutputType>
Operation<InputType, OutputType>::Operation(string name) 
{
  // Bouml preserved body begin 00021B11

	operationName = name;

  // Bouml preserved body end 00021B11
}

template<typename InputType, typename OutputType>
Operation<InputType, OutputType>::~Operation() 
{
  // Bouml preserved body begin 0005A591
  // Bouml preserved body end 0005A591
}


} // namespace lpm
#endif
