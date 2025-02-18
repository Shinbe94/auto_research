
#Running a command as Administrator using PowerShell
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))  
{  
  $arguments = "& '" +$myinvocation.mycommand.definition + "'"
  Start-Process powershell -Verb runAs  -ArgumentList $arguments
  Break
}


$path = "C:\Program Files (x86)\CocCoc\"
$path1 = "C:\Program Files\CocCoc\"



if (Test-Path $path) 
		{ 
		
		
			if ( Test-Path $path1)
				{	
					
					"--------------------------------------------------------------------------------------------------------------------------------"
					"You installed Coc Coc browser x64 on 64-bit operating system"
					"--------------------------------------------------------------------------------------------------------------------------------"
					$getFiles = Get-ChildItem -Recurse -Path $path -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -ne 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }	
					
						if ($getFiles -eq $null ) {
							"--------------------------------------------------------------------------------------------------------------------------------"
							
							Get-ChildItem -Recurse -Path $path -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -eq 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							"--------------------------------------------------------------------------------------------------------------------------------"
							#"Get the name of the signer from a signed file"
							#Get-AppLockerFileInformation -Directory $path -Recurse -FileType exe, dll | select Path,Publisher		
							"--------------------------------------------------------------------------------------------------------------------------------"	
							"Test passed, no file has invalid sig at $path"
							"--------------------------------------------------------------------------------------------------------------------------------"
				
						}
						else {
							"--------------------------------------------------------------------------------------------------------------------------------"
							Get-ChildItem -Recurse -Path $path -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -eq 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							"--------------------------------------------------------------------------------------------------------------------------------"
							Write-Warning "Test FAILED: Here is the list that has a problem with signature at $path"
							"--------------------------------------------------------------------------------------------------------------------------------"
							Get-ChildItem -Recurse -Path $path -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -ne 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
						}
					
					
					"--------------------------------------------------------------------------------------------------------------------------------"	
				
					
					$getFiles1 = Get-ChildItem -Recurse -Path $path1 -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -ne 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }	
					
						if ($getFiles1 -eq $null ) {
							"--------------------------------------------------------------------------------------------------------------------------------"
							
							Get-ChildItem -Recurse -Path $path1 -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -eq 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							"--------------------------------------------------------------------------------------------------------------------------------"
							#"Get the name of the signer from a signed file"
							#Get-AppLockerFileInformation -Directory $path1 -Recurse -FileType exe, dll | select Path,Publisher
							"--------------------------------------------------------------------------------------------------------------------------------"
							"Test passed, no file has invalid sig at $path1"
							"--------------------------------------------------------------------------------------------------------------------------------"
						}
						else {
							"--------------------------------------------------------------------------------------------------------------------------------"
							Get-ChildItem -Recurse -Path $path1 -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -eq 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							"--------------------------------------------------------------------------------------------------------------------------------"
							Write-Warning "Test FAILED: Here is the list that has a problem with signature at $path1"
							"--------------------------------------------------------------------------------------------------------------------------------"
							Get-ChildItem -Recurse -Path $path1 -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -ne 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							
						} 
						"--------------------------------------------------------------------------------------------------------------------------------"				
				
				}
			else 
				{
					"--------------------------------------------------------------------------------------------------------------------------------"
					"You installed Coc Coc browser x86 on 64-bit operating system"
					$getFiles = Get-ChildItem -Recurse -Path $path -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -ne 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }	
					
						if ($getFiles -eq $null ) {
							"--------------------------------------------------------------------------------------------------------------------------------"
							
							
							Get-ChildItem -Recurse -Path $path -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -eq 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							"--------------------------------------------------------------------------------------------------------------------------------"
							#"Get the name of the signer from a signed file"
							#Get-AppLockerFileInformation -Directory $path -Recurse -FileType exe, dll | select Path,Publisher
							"--------------------------------------------------------------------------------------------------------------------------------"
							"Test passed, no file has invalid sig at $path"
							"--------------------------------------------------------------------------------------------------------------------------------"
						}
						else {
							
							Get-ChildItem -Recurse -Path $path -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -eq 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							"--------------------------------------------------------------------------------------------------------------------------------"
							Write-Warning "Test FAILED: Here is the list that has a problem with signature at $path"
							"--------------------------------------------------------------------------------------------------------------------------------"
							Get-ChildItem -Recurse -Path $path -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -ne 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							
						}	"--------------------------------------------------------------------------------------------------------------------------------"
					

				}
		}
		
else {
		"--------------------------------------------------------------------------------------------------------------------------------"
			"You installed Coc Coc browser x86 on 32-bit operating system"
			"--------------------------------------------------------------------------------------------------------------------------------"
			$getFiles1 = Get-ChildItem -Recurse -Path $path1 -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -ne 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }	
					
						if ($getFiles1 -eq $null ) {
							"--------------------------------------------------------------------------------------------------------------------------------"
							"Test passed, no file has invalid sig at $path1"
							"--------------------------------------------------------------------------------------------------------------------------------"
							#"Get the name of the signer from a signed file"
							#Get-AppLockerFileInformation -Directory $path1 -Recurse -FileType exe, dll | select Path,Publisher
							"--------------------------------------------------------------------------------------------------------------------------------"
 						}
						else {
							"--------------------------------------------------------------------------------------------------------------------------------"
							Get-ChildItem -Recurse -Path $path1 -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -eq 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							"--------------------------------------------------------------------------------------------------------------------------------"
							
							Write-Warning "Test FAILED: Here is the list that has a problem with signature at $path"
							"--------------------------------------------------------------------------------------------------------------------------------"
							Get-ChildItem -Recurse -Path $path1 -Include *.dll, *.exe| ForEach-object {(Get-AuthenticodeSignature $_.FullName)} | Where-Object { $_.Status -ne 'Valid' } | ForEach-Object { '{0} {1}' -f $_.Status, $_.Path }
							
						} 
		
	}
									


pause