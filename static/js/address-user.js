const countryCurrent = document.getElementById(
  'id_temporary_address-0-country'
);
const provinceCurrent = document.getElementById(
  'id_temporary_address-0-province'
);
const districtCurrent = document.getElementById(
  'id_temporary_address-0-district'
);
const vdcCurrent = document.getElementById(
  'id_temporary_address-0-vdc_municipality'
);
const wardNoCurrent = document.getElementById(
  'id_temporary_address-0-ward_number'
);

const countryPermanent = document.getElementById(
  'id_permanent_address-0-country'
);
const provincePermanent = document.getElementById(
  'id_permanent_address-0-province'
);
const districtPermanent = document.getElementById(
  'id_permanent_address-0-district'
);
const vdcPermanent = document.getElementById(
  'id_permanent_address-0-vdc_municipality'
);
const wardNoPermanent = document.getElementById(
  'id_permanent_address-0-ward_number'
);

const provinceDefaultOptionText = '(Select Province)';
const districtDefaultOptionText = '(Select District)';
const vdcDefaultOptionText = '(Select VDC/Municipality)';
const wardNoDefaultOptionText = '(Select Ward Number)';

Element.prototype.remove = function () {
  this.parentElement.removeChild(this);
};

HTMLSelectElement.prototype.addOption = function (optionValue, optionText) {
  const node = document.createElement('option');
  node.value = optionValue;
  node.innerText = optionText;
  this.appendChild(node);
};

HTMLSelectElement.prototype.assignChildNodes = function (rootChildNodes) {
  for (var i = 0; i < rootChildNodes.length; i++) {
    let tempNode = rootChildNodes[i].cloneNode(true);
    this.appendChild(tempNode);
  }
};

NodeList.prototype.remove = HTMLCollection.prototype.remove = function () {
  while (this[0]) {
    this[0].remove();
  }
};

HTMLSelectElement.prototype.copy = function (rootElement) {
  this.childNodes.remove();
  this.assignChildNodes(rootElement.childNodes);
  this.value = rootElement.value;
};

NodeList.prototype.removeExcept = function (optiontext) {
  while (this[0]) {
    if (this[0].text != optiontext) {
      this[0].remove();
    } else if (this[1]) {
      this[1].remove();
    } else {
      break;
    }
  }
};

updateProvince = function (addresstype) {
  if (addresstype === 'Current') {
    provinceCurrent.childNodes.removeExcept(provinceDefaultOptionText);
    districtCurrent.childNodes.removeExcept(districtDefaultOptionText);
    vdcCurrent.childNodes.removeExcept(vdcDefaultOptionText);
    wardNoCurrent.childNodes.removeExcept(wardNoDefaultOptionText);

    var provinceSelect = provinceCurrent;
    var country = countryCurrent.value;
  } else if (addresstype === 'Permanent') {
    provincePermanent.childNodes.removeExcept(provinceDefaultOptionText);
    districtPermanent.childNodes.removeExcept(districtDefaultOptionText);
    vdcPermanent.childNodes.removeExcept(vdcDefaultOptionText);
    wardNoPermanent.childNodes.removeExcept(wardNoDefaultOptionText);

    var provinceSelect = provincePermanent;
    var country = countryPermanent.value;
  }

  if (!country) return;
  return fetch(`/getProvince/${country}`)
    .then((res) => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
    .then((data) => {
      data.forEach((el) => {
        provinceSelect.addOption(el[0], el[1]);
      });
      updateDistrict(addresstype);
    })
    .catch((err) => {
      console.error(
        'There has been a problem with your fetch operation: ',
        err.message
      );
    });
};

updateDistrict = function (addresstype) {
  if (addresstype === 'Current') {
    districtCurrent.childNodes.removeExcept(districtDefaultOptionText);
    vdcCurrent.childNodes.removeExcept(vdcDefaultOptionText);
    wardNoCurrent.childNodes.removeExcept(wardNoDefaultOptionText);

    var districtSelect = districtCurrent;
    var province = provinceCurrent.value;
  } else if (addresstype === 'Permanent') {
    districtPermanent.childNodes.removeExcept(districtDefaultOptionText);
    vdcPermanent.childNodes.removeExcept(vdcDefaultOptionText);
    wardNoPermanent.childNodes.removeExcept(wardNoDefaultOptionText);

    var districtSelect = districtPermanent;
    var province = provincePermanent.value;
  }

  if (!province) return;
  return fetch(`/getDistrict/${province}`)
    .then((res) => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
    .then((data) => {
      data.forEach((el) => {
        districtSelect.addOption(el[0], el[1]);
      });
      updateVDCMunicipality(addresstype);
    })
    .catch((err) => {
      console.error(
        'There has been a problem with your fetch operation: ',
        err.message
      );
    });
};

updateVDCMunicipality = function (addresstype) {
  if (addresstype === 'Current') {
    vdcCurrent.childNodes.removeExcept(vdcDefaultOptionText);
    wardNoCurrent.childNodes.removeExcept(wardNoDefaultOptionText);

    var vdcMunicipalitySelect = vdcCurrent;
    var district = districtCurrent.value;
  } else if (addresstype === 'Permanent') {
    vdcPermanent.childNodes.removeExcept(vdcDefaultOptionText);
    wardNoPermanent.childNodes.removeExcept(wardNoDefaultOptionText);

    var vdcMunicipalitySelect = vdcPermanent;
    var district = districtPermanent.value;
  }

  if (!district) return;
  return fetch(`/getVDCMunicipality/${district}`)
    .then((res) => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
    .then((data) => {
      data.forEach((el) => {
        vdcMunicipalitySelect.addOption(el[0], el[1]);
      });
      updateWardNumber(addresstype);
    })
    .catch((err) => {
      console.error(
        'There has been a problem with your fetch operation: ',
        err.message
      );
    });
};

updateWardNumber = function (addresstype) {
  if (addresstype === 'Current') {
    wardNoCurrent.childNodes.removeExcept(wardNoDefaultOptionText);

    var wardNoSelect = wardNoCurrent;
    var vdcMunicipality = vdcCurrent.value;
  } else if (addresstype === 'Permanent') {
    wardNoPermanent.childNodes.removeExcept(wardNoDefaultOptionText);

    var wardNoSelect = wardNoPermanent;
    var vdcMunicipality = vdcPermanent.value;
  }

  if (!vdcMunicipality) return;
  return fetch(`/getWardNumber/${vdcMunicipality}`)
    .then((res) => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
    .then((data) => {
      data.forEach((el) => {
        wardNoSelect.addOption(el[0], el[1]);
      });
    })
    .catch((err) => {
      console.error(
        'There has been a problem with your fetch operation: ',
        err.message
      );
    });
};

async function setAddressInitial() {
  await updateProvince('Current');
  await updateProvince('Permanent');

  if (currentCountryValue) {
    /**
     * The array of the options of the corresponding dropdowns are obtained using the spread (...)
     * operator and findIndex(condition) is used to return the index of the value (in the dropdown),
     * retrieved from the context.
     */
    document.querySelectorAll(`#delete-row-button`)[1].parentElement.click();

    const experienceLength = roles.length;
    for (let i = 0; i < experienceLength; i++) {
      if (i) document.getElementById('add-row-button').parentElement.click();
      const roleInput = document.getElementById(`id_experience-${i}-role`);
      const noOfYearsInput = document.getElementById(
        `id_experience-${i}-no_of_years`
      );
      roleInput.value = roles.shift();
      noOfYearsInput.value = noOfYears.shift();
    }

    countryCurrent.selectedIndex = [...countryCurrent.options].findIndex(
      (option) => option.text === currentCountryValue
    );

    await updateProvince('Current');
    provinceCurrent.selectedIndex = [...provinceCurrent.options].findIndex(
      (option) => option.text === currentProvinceValue
    );

    await updateDistrict('Current');
    districtCurrent.selectedIndex = [...districtCurrent.options].findIndex(
      (option) => option.text === currentDistrictValue
    );

    await updateVDCMunicipality('Current');
    vdcCurrent.selectedIndex = [...vdcCurrent.options].findIndex(
      (option) => option.text === currentVdcValue
    );

    await updateWardNumber('Current');
    wardNoCurrent.selectedIndex = [...wardNoCurrent.options].findIndex(
      (option) => option.text === currentWardNoValue
    );

    countryPermanent.selectedIndex = [...countryPermanent.options].findIndex(
      (option) => option.text === permanentCountryValue
    );

    await updateProvince('Permanent');
    provincePermanent.selectedIndex = [...provincePermanent.options].findIndex(
      (option) => option.text === permanentProvinceValue
    );

    await updateDistrict('Permanent');
    districtPermanent.selectedIndex = [...districtPermanent.options].findIndex(
      (option) => option.text === permanentDistrictValue
    );

    await updateVDCMunicipality('Permanent');
    vdcPermanent.selectedIndex = [...vdcPermanent.options].findIndex(
      (option) => option.text === permanentVdcValue
    );

    await updateWardNumber('Permanent');
    wardNoPermanent.selectedIndex = [...wardNoPermanent.options].findIndex(
      (option) => option.text === permanentWardNoValue
    );
  }
}

window.addEventListener('load', async (event) => {
  // await updateProvince('Current');
  // await updateProvince('Permanent');
  // addressTypeCurrent.value = 'Current';
  // document.getElementById('div_id_address-0-type').style.display = 'none';
  // const addressTypeCurrentText = document.getElementById('address-type-0');
  // addressTypeCurrentText.innerHTML = 'CURRENT ADDRESS';
  // addressTypePermanent.value = 'Permanent';
  // document.getElementById('div_id_address-1-type').style.display = 'none';
  // const addressTypePermanentText = document.getElementById('address-type-1');
  // addressTypePermanentText.innerHTML = 'PERMANENT ADDRESS';
  // const checkboxDiv = document.getElementById('checkbox-div-1');
  // checkboxDiv.innerHTML = `<div class="custom-control custom-checkbox pb-3">
  //     <input type="checkbox" class="custom-control-input" id="same-permanent" onclick="sameAsCurrent()">
  //     <label class="custom-control-label" for="same-permanent">
  //     Same as Current
  //     </label>
  //     </div>`;
  setAddressInitial();
});

countryCurrent.addEventListener('change', (event) => {
  updateProvince('Current');
});
provinceCurrent.addEventListener('change', (event) => {
  updateDistrict('Current');
});
districtCurrent.addEventListener('change', (event) => {
  updateVDCMunicipality('Current');
});
vdcCurrent.addEventListener('change', (event) => {
  updateWardNumber('Current');
});

countryPermanent.addEventListener('change', (event) => {
  updateProvince('Permanent');
});
provincePermanent.addEventListener('change', (event) => {
  updateDistrict('Permanent');
});
districtPermanent.addEventListener('change', (event) => {
  updateVDCMunicipality('Permanent');
});
vdcPermanent.addEventListener('change', (event) => {
  updateWardNumber('Permanent');
});
